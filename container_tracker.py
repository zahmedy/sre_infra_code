import heapq
from collections import deque

class ContainerTracker:
    def __init__(self, max_window_size: int = 10000):
        self.max_window_size = max_window_size
        self.trackers = dict()

    def record_cpu(self, container_id: str, cpu_percent: float) -> None:
        """
        Records a new CPU utilization reading for a specific container.
        This is called continuously by our metrics collector daemon.
        """
        if container_id not in self.trackers:
            self.trackers[container_id] = {
                "max_heap": [],         # Lower half
                "min_heap": [],         # Upper half
                "history": deque(),     # Tracks chronological arrival order
                "expired": dict(),      # Tracks counts of items waiting to be deleted 
                "valid_max_count": 0,   # Active item counters
                "valid_min_count": 0
            }
    
        c = self.trackers[container_id]

        # Step 1: If our window is completely full, evict the oldest element
        if len(c["history"]) >= self.max_window_size:
            oldest_value = c["history"].popleft()
            # Mark it as expired so the heaps know to ignore it when it hits the top
            c["expired"][oldest_value] = c["expired"].get(oldest_value, 0) + 1

            # Decrement our active counts depending on where the old value lives
            if c["max_heap"] and oldest_value <= -c["max_heap"][0]:
                c["valid_max_count"] -= 1
            else:
                c["valid_min_count"] -= 1

        # Step 2: Ingest the new element chronologically
        c["history"].append(cpu_percent)

        # Step 3: Route into out dual heap 
        if not c["max_heap"] or cpu_percent <= -c["max_heap"][0]:
            heapq.heappush(c["max_heap"], -cpu_percent)
            c["valid_max_count"] += 1
        else:
            heapq.heappush(c["min_heap"], cpu_percent)
            c["valid_min_heap"] += 1

        # Rebalance step: Ensure sizes don't differ by more than 1
        if len(c["valid_max_count"]) > len(c["valid_min_count"]) + 1:
            val = -heapq.heappop(c["max_heap"])
            c["valid_max_heap"] -= 1
            heapq.heappush(c["min_heap"], val)
            c["valid_min_count"] += 1
        elif len(c["valid_min_count"]) > len(c["valid_max_count"]) + 1:
            val = heapq.heappop(c["min_heap"])
            c["valid_min_heap"] -= 1
            heapq.heappush(c["max_heap"], -val)
            c["valid_max_heap"] += 1


    def _prune_heap_tops(self, c: dict) -> None:
        """Helper to lazily discard expired elements currently sitting at the tops."""
        # Clean max heap top
        while c["max_heap"]:
            top_val = -c["max_heap"][0]
            if c["expired"].get(top_val, 0) > 0:
                heapq.heappop(c["max_heap"])
                c["expired"][top_val] -= 1
            else:
                break

        # Clean min heap
        while c["min_heap"]:
            top_val = c["min_heap"][0]
            if c["expired"].get(top_val, 0) > 0:
                heapq.heappop(c["min_heap"])
                c["expired"][top_val] -= 1
            else:
                break

    def get_median_cpu(self, container_id: str) -> float:
        """
        Returns the exact median CPU utilization recorded for the container so far.
        If no metrics exist for the container, return 0.0.
        """
        if container_id not in self.trackers:
            return 0.0
        
        c = self.trackers[container_id]

        # Clean out any dead metrics sitting at the tops before evaluating median 
        self._prune_heap_tops(c)

        if c["valid_max_count"] == 0 and c["valid_min_count"] == 0:
            return 0.0

        # Extract accurate median from pristine tops
        if c["valid_max_count"] > c["valid_min_count"]:
            return -c["max_heap"][0]

        elif c["valid_min_count"] < c["valid_max_count"]:
            return c["min_heap"][0]
        
        else:
            return (-c["max_heap"][0] + c["min_heap"][0]) / 2.0
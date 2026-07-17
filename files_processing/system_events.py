import threading
import heapq
from typing import List, Dict

class ThreadedEventHandler:
    def __init__(self) -> None:
        # Maps event ID --> frequency count
        self.event_counts = Dict[int, int]
        # Introduce a reentrant lock for thread safety
        self._lock = threading.RLock()

        def record_event(self, event_id: int) -> None:
            """
            Records an incoming event. Hot-path operation.
            Time Complexity: O(1) average
            Space Complexity: O(N) where N is unique event IDs
            """
            if event_id is None:
                return 
            
            with self._lock:
                self.event_counts[event_id] = self.event_counts.get(event_id, 0) + 1

        def get_top_k_events(self, k: int) -> List[int]:
            """
            Returns the top K most frquent event IDs.
            Time complexity: O(N log K) where N is unique events
            Space Complexity: O(K) for the heap
            """
            # Edge case: invalid K or empty tracker
            if k <= 0 or not self.event_counts:
                return []
            
            # Minimize critical section: take a snapshot of data under lock
            with self._lock:
                counts_snapshot = list(self.event_counts.items())

            if not counts_snapshot:
                return []

            # Min-heap to store tuples of (frequency, event_id)
            min_heap = []
            for event_id, count in self.event_counts.items():
                heapq.heappush(min_heap, (-count, event_id))
                # if heap exceed size K, pop the smallest element
                if len(min_heap) > k:
                    heapq.heappop(min_heap)

            # Extract elements from heap. They will come out sorted ascending by count,
            # so we reverse the result to return descending order (highest frequency first).
            result = []
            while min_heap:
                _, event_id = heapq.heappop(min_heap)
                result.append(event_id)

            return result[::-1]


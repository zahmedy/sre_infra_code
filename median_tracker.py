import heapq

class MedianTracker:
    def __init__(self):
        self.min_heap = []
        self.max_heap = []

    def add_number(self, num: int) -> None:
        """ Adds a number from the data stream into the structure. """
        if not self.max_heap or num <= self.max_heap[0]:
            heapq.heappush(self.max_heap, -num)
        else:
            heapq.heappush(self.min_heap, num)

        # Balance check 
        if len(self.max_heap) > len(self.min_heap) + 1:
            val = heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, -val)
        elif len(self.max_heap) + 1 < len(self.min_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)
        

    def find_median(self) -> float:
        """ Returns the median of all elements saw so far in O(1). """
        if len(self.max_heap) > len(self.min_heap):
            return float(-self.max_heap[0])
        elif len(self.max_heap) < len(self.min_heap):
            return float(self.min_heap[0])
        
        return (-self.max_heap[0] + self.min_heap[0]) / 2.0
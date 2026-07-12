class ErrorCounter:
    def __init__(self):
        self.timestamps = [-1] * 300
        self.counts = [0] * 300

    def record(self, timestamp: int) -> None:
        index = timestamp % 300
        
        if self.timestamps[index] != timestamp:
            self.timestamps[index] = timestamp
            self.counts[index] = 0

        self.counts[index] += 1

    def count(self, timestamp: int) -> int:
        total_errors = 0
        window_start = timestamp - 299

        for index in range(300):
            stored_timestamp = self.timestamps[index]

            if  window_start <= stored_timestamp <= timestamp:
                total_errors += self.counts[index]

        return total_errors
    

requests = [3, 1, 4, 2, 6, 1]
k = 3
threshold = 11

def earliest_overloaded_window(
    requests: list[int],
    k: int,
    threshold: int
) -> int:
    if not requests or k <= 0 or k > len(requests):
        return -1
    
    window_sum = sum(requests[:k])

    if window_sum >= threshold:
        return 0

    for right in range(k, len(requests)):
        left = right - k

        window_sum -= requests[left]
        window_sum += requests[right]

        if window_sum >= threshold:
            return left + 1

    return -1
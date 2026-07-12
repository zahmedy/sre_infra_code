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

from typing import Iterable
from collections import deque, defaultdict

def first_frequent_error(
    logs: Iterable[tuple[int, str]],
    k: int
) -> str | None:
    if k <= 0:
        raise ValueError("K must be greater than 0")
    
    counter = defaultdict(int)
    errors_pipe = deque()

    for timestamp, error_code in logs:
        window_start = timestamp - 59

        while errors_pipe and errors_pipe[0][0] < window_start:
            _, expired_code = errors_pipe.popleft()
            counter[expired_code] -= 1

            if counter[expired_code] == 0:
                del counter[expired_code]

        errors_pipe.append((timestamp, error_code))
        counter[error_code] += 1

        if counter[error_code] >= k:
            return error_code

    return None

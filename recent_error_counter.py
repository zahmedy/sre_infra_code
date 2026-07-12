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


def minimum_servers(jobs: list[list[int]]) -> int:
    """
    Return minimum number of servers to run deployement jobs ex: 
    jobs = [[0, 30],[5, 10],[15, 20],[20, 25]]
    Output: 2
    I use sweep-line approache to solve this
    """
    if not jobs:
        return 0
    
    events = []

    for start_time, end_time in jobs:
        events.append((start_time, 1))
        events.append((end_time, -1))

    # Sort by start time first if identical sort by change
    events = sorted(
        events,
        key=lambda x: (x[0], x[1])
    )

    max_servers = 0
    current_servers = 0

    for _, change in events:
        current_servers += change
        max_servers = max(max_servers, current_servers)

    return max_servers


def merge_maintenance_windows(
    windows: list[list[int]]
) -> list[list[int]]:
    """
    Merge overlapping maintanence windows 
    Example Input: windows = [[1, 4], [2, 6], [8, 10],[10, 12]]
    Output: [[1, 6], [8, 12]]
    """
    if not windows:
        return []

    # Sort by start time only
    windows = sorted(windows, key=lambda interval: interval[0])
    merged: list[list[int]] = []

    for start, end in windows:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return merged

def shortest_recovery_path(
    grid: list[list[int]],
    start: tuple[int, int],
    target: tuple[int, int]
) -> int:
    if not grid or not grid[0]:
        return -1
    
    rows, cols = len(grid), len(grid[0])
    
    def is_valid_position(position: tuple[int, int]) -> bool:
        row, col = position
        return 0 <= row < rows and 0 <= col < cols
    
    if not is_valid_position(start) or not is_valid_position(target):
        return -1
    
    start_row, start_col = start
    target_row, target_col = target

    if grid[start_row][start_col] != 0:
        return -1
    
    if grid[target_row][target_col] != 0:
        return -1
    
    if start == target:
        return 0
    
    queue = deque([(start_row, start_col, 0)])
    visited = {start}

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    while queue:
        row, col, steps = queue.popleft()

        if (row, col) == target:
            return steps

        for n_row, n_col in directions:
            new_row = row+n_row
            new_col = col+n_col
            position = (new_row, new_col)
            if (
                is_valid_position(position) 
                and grid[new_row][new_col] == 0
                and position not in visited
            ):
                visited.add(position)
                queue.append((new_row, new_col ,steps+1))

    return -1
    

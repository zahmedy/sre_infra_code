def merge_outages(intervals: list[list[int]]) -> list[list[int]]:
    merged = []

    for start, end in sorted(intervals, key=lambda interval: interval[0]):
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return merged


requests = [
    "host-1",
    "host-2",
    "host-1",
    "host-3",
    "host-2",
    "host-1",
]

from collections import Counter

def top_k_hosts(requests: list[str], k: int) -> list[str]:
    if k <= 0:
        return []

    counts = Counter(requests)

    hosts = sorted(
        counts,
        key=lambda host: (-counts[host], host)
    )

    return hosts[:k]

jobs = [
    [1, 4],
    [2, 5],
    [7, 9],
    [3, 6],
]

def min_servers(jobs: list[list[int]]) -> int:
    events = []

    # Break the events to start and end times
    # 1 means server busy -1 mean it is free
    for start, end in jobs:
        events.append((start, 1))
        events.append((end, -1))

    # If times are equal, end event (-1) come before start events (1)
    events.sort(key=lambda x: (x[0], x[1]))

    max_servers = 0
    current_servers = 0

    for _, change in events:
        current_servers += change
        if current_servers > max_servers:
            max_servers = current_servers
    
    return max_servers


[3, 4, -1, 1]  # returns 2
[1, 2, 0]      # returns 3
[7, 8, 9, 11]  # returns 1


def first_missing_positive(nums: list[int]) -> int:
    n = len(nums)

    for i in range(n):
        # While the current number is a valid positive number within range
        # and is NOT currently setting at its correct 'home' index
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            # Swap it to its correct home index: nums[i] - 1
            correct_idx = nums[i] - 1
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]

    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
        
    return n + 1

from collections import deque

def minimum_startup_time(
    n: int,
    durations: list[int],
    dependencies: list[list[int]]
) -> int:
        
    indegree = [0] * n
    dependents = [[] for _ in range(n)]

    for service, prerequisite in dependencies:
        indegree[service] += 1
        dependents[prerequisite].append(service)

    queue = deque(
        service for service in range(n) 
        if indegree[service] == 0
    )

    processed_services = 0
    completion_time = durations.copy()

    while queue:
        prerequisite = queue.popleft()
        processed_services += 1

        for service in dependents[prerequisite]:
            completion_time[service] = max(
                completion_time[service],
                completion_time[prerequisite] + durations[service]
            )
            indegree[service] -= 1

            if indegree[service] == 0:
                queue.append(service)
    
    if processed_services != n:
        return -1
    
    return max(completion_time)


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
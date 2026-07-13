from collections.abc import Iterable
import re

def services_to_rollback(
    events: Iterable[str],
    failure_percentage: float,
    minimum_hosts: int,
) -> list[str]:
    services = {}

    pattern = re.compile(r"^(service-[a-z]+)\s+(host-[0-9]+)\s+(SUCCESS|FAILURE)$")

    for event in events:
        match = pattern.fullmatch(event)
        if not match:
            continue

        service, host, stat = match.groups()
        services.setdefault(service, {})[host] = stat

    rollback = []

    for service, hosts in services.items():
        total_hosts = len(hosts)

        if total_hosts < minimum_hosts:
            continue

        failed_hosts = sum(
            status == "FAILURE"
            for status in hosts.values()
        )

        failure_rate = failed_hosts / total_hosts * 100

        if failure_rate  >= failure_percentage:
            rollback.append(service)

    return sorted(rollback)

import heapq
from collections import Counter, defaultdict
from collections.abc import Iterable

def top_k_failing_services(
    failures: list[str],
    k: int
) -> list[str]:
    """
    Using min-heap to return top K failing services 
    for efficient O(N log K) because we only keep k element in the heap
    """
    if k <= 0 or not failures:
        return []

    min_heap = []
    counts = Counter(failures)

    for service, count in counts.items():
        heapq.heappush(min_heap, (count, service))

        if len(min_heap) > k:
            heapq.heappop(min_heap)

    ordered = sorted(min_heap, reverse=True)
    return [service for _,service in ordered]
    
class FailureTracker:
    def __init__(self) -> None:
        self.counts = defaultdict(int)
        self.max_heap = []

    def record_failure(self, service: str) -> None:
        self.counts[service] += 1
        current_count = self.counts[service]

        heapq.heappush(
            self.max_heap,
            (-current_count, service)
        )
    
    def top_k(self, k: int) -> list[str]:
        result = []
        valid_entries = []

        while self.max_heap and len(result) < k:
            negative_count, service = heapq.heappop(self.max_heap)
            stored_count = - negative_count
            
            if stored_count != self.counts[service]:
                continue

            result.append(service)
            valid_entries.append((negative_count, service))

        for entry in valid_entries:
            heapq.heappush(self.max_heap, entry)

        return result

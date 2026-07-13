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
from collections import Counter

def top_k_failing_services(
    failures: list[str],
    k: int
) -> list[str]:
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
    


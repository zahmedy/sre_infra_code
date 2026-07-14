from collections.abc import Iterable
from collections import Counter
import re

def overloaded_hosts(
    events: Iterable[str],
    threshold: int,
    consecutive_count: int,
) -> list[str]:
    overloaded = set()
    streak = Counter()

    pattern = re.compile(
        r"^(host-[0-9]+)\s+([0-9]{1,3})$"
    )

    for event in events:
        match = pattern.fullmatch(event)

        if not match:
            continue

        host = match.group(1)
        cpu = int(match.group(2))

        if not 0 <= cpu <= 100:
            continue

        if cpu >= threshold:
            streak[host] += 1
        else:
            streak[host] = 0

        if streak[host] >= consecutive_count:
            overloaded.add(host)

    return sorted(overloaded)
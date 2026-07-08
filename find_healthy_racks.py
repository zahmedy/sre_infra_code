from collections.abc import Iterable
from collections import Counter
from datetime import datetime
import re

def find_unhealthy_racks(
    events: Iterable[str],
    threshold: int
) -> list[str]:
    hosts = {}

    pattern = re.compile(
        r"(?P<date>^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)\s+"
        r"(?P<host>host-[0-9]+)\s+"
        r"(?P<rack>rack-[a-z]+)\s+"
        r"(?P<stat>UP|DOWN)$"
    )

    for event in events:
        match = pattern.fullmatch(event)

        date, host, rack, stat = None, None, None, None
        if not match:
            continue

        try:
            date = datetime.fromisoformat(match.group('date'))
        except ValueError:
            continue
        host = match.group('host')
        rack = match.group('rack')
        stat = match.group('stat')
        
        if host in hosts:
            # Is this a newer event?
            curr_time = hosts[host]["date"]
            if date > curr_time:
                hosts[host]["date"] = date
                hosts[host]["stat"] = stat
                hosts[host]["rack"] = rack

        else:
            hosts[host] = { "date": date, "rack": rack, "stat": stat }

    counter = Counter()
    for host in hosts:
        if hosts[host]["stat"] == "DOWN":
            counter[hosts[host]["rack"]] += 1

    return sorted(rack for rack, count in counter.items() if count >= threshold)
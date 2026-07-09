from collections.abc import Iterable
from collections import deque
import re

def find_flapping_hosts(events: Iterable[str],window_size: int,transition_threshold: int) -> list[str]:
    if window_size < 2:
        return []
    
    history = {}

    pattern = re.compile(
        r"(?P<host>^host-[0-9]+)\s+"
        r"(?P<stat>FAIL|PASS)$"
    )

    for event in events:
        match = pattern.fullmatch(event)

        if not match:
            continue

        host, stat = None, None
        host = match.group('host')
        stat = match.group('stat')

        if host not in history:
            history[host] = {
                "queue": deque(maxlen=window_size),
                "transitions": 0
                }
            
        queue = history[host]["queue"]
        transitions = history[host]["transitions"]
        
        if len(queue) == window_size:
            if queue[0] != queue[1]:
                transitions -=1
            queue.popleft()
        
        if queue and queue[-1] != stat:
            transitions +=1

        queue.append(stat)
        history[host]["transitions"] = transitions


    return sorted(
        host
        for host, data in history.items()
        if len(data["queue"]) == window_size
        and data["transitions"] >= transition_threshold
    )
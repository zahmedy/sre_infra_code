import time
from collections import deque
import threading

class ThreadSafeRateLimiter:
    def __init__(self, max_requests: int, window_size_second: int):
        """
        max_requests (M): Max allowed requests in the window
        window_size_second (T): The sliding window duration 
        """
        self.max_requests = max_requests
        self.window_size = window_size_second
        self.ip_window_tracker = dict()
        self._master_lock = threading.Lock()

    def allow_request(self, ip_address: str) -> bool:
        current_time = time.time()

        # init the Queue if empty
        if ip_address not in self.ip_window_tracker:
            with self._master_lock:
                # Double-check pattern to prevent race conditions during initialization
                if ip_address not in self.ip_window_tracker:
                    self.ip_window_tracker[ip_address] = {
                        "queue": deque(),
                        "lock": threading.Lock() # Fine-grained lock per IP!
                    }
        
        ip_data = self.ip_window_tracker[ip_address]

        # Phase 2: Lock ONLY this specific IP's data
        with ip_data["lock"]:
            history = ip_data["queue"]

            # EVICT EXIRED timestamp before processing the new request
            while history and (current_time - history[0] > self.window_size):
                history.popleft()

            # check if the IP has remaining capcity 
            if len(history) < self.max_requests:
                history.append(current_time)
                return True

        return False
    
class RateLimiter:
    def __init__(self, k) -> None:
        self.k = k
        self.tracker: dict[str, deque[int]] = {}
    
    def allow(self, user: str, timestamp: int) -> bool:
        if user not in self.tracker:
            self.tracker[user] = deque()
        
        queue = self.tracker[user]
        window_start = timestamp - 59

        while queue and queue[0] < window_start:
            queue.popleft()

        if len(queue) >= self.k:
            return False

        queue.append(timestamp)
        return True
    
def sorted_longest_failure_streak(failures: list[int]) -> int:
    if not failures:
        return 0

    current_streak = 1
    max_streak = 1

    for i in range(1, len(failures)):
        if failures[i] == failures[i - 1] + 1:
            current_streak += 1
        else:
            current_streak = 1

        max_streak = max(max_streak, current_streak)

    return max_streak

def unsorted_longest_failure_streak(failures: list[int]) -> int:
    if not failures:
        return 0
    
    failures_set = set(failures)
    max_streak = 0

    for timestamp in failures_set:
        # Check if timestamp start of a streak 
        if timestamp - 1 not in failures_set:
            current_timestamp = timestamp
            current_streak = 1

            while current_timestamp + 1 in failures_set:
                current_timestamp += 1
                current_streak +=1
                
            max_streak = max(max_streak, current_streak)

    return max_streak

        





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
import time
import threading

class TokenBucketLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        """
        capacity: Maximum tokens the bucket can hold.
        refill_rate: How many tokens are added per second.
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last_update_time = time.time()
        self.lock = threading.Lock()

    def allow_request(self) -> bool:
        with self.lock:
            current_time = time.time()

            # Update tokens first
            tokens_to_add = (current_time - self.last_update_time) * self.refill_rate
            self.tokens = min(float(self.capacity), self.tokens + tokens_to_add)

            self.last_update_time = current_time

            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True       

            return False
        
# This is a conceptual look at how a distributed architecture operates.
# Instead of Python code executing locally, we send this command to Redis:

# 1. Fetch current token count and last update timestamp from Redis
# 2. Run the exact same math we designed: 
#    tokens = min(capacity, current_tokens + (now - last_time) * refill_rate)
# 3. If tokens >= 1, decrement by 1, save back to Redis, and return True
# 4. Otherwise, return False
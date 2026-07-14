from collections.abc import Callable
import time
import random

class TemporaryError(Exception):
    pass

def run_with_retries(
    operation: Callable[[], bool],
    max_attempts: int,
    base_delay: float,
    timeout_seconds: float
) -> bool:
    if max_attempts <= 0:
        return False
    
    if base_delay < 0 or timeout_seconds < 0:
        raise ValueError("base_delay and timeout_seconds must be non-negative")
    
    deadline = time.monotonic() + timeout_seconds

    for attempt in range(max_attempts):
        if time.monotonic() >= deadline:
            return False
        
        try:
            if operation():
                return True
        except TemporaryError:
            pass
        except Exception:
            raise

        is_final_attempt = attempt == max_attempts - 1
        if is_final_attempt:
            break

        exponential_delay = base_delay * (2 ** attempt)

        # Full jitter: random delay between 0 and backoff limit
        delay = random.uniform(0, exponential_delay)

        remaining_time = deadline - time.monotonic()
        if remaining_time <= 0:
            return False

        # Never sleep beyond the deadline 
        time.sleep(min(delay, remaining_time))

    return False
from collections.abc import Callable
import time

def run_with_retries(
    operation: Callable[[], bool],
    max_attempts: int,
    base_delay: float,
) -> bool:
    
    for attempt in range(max_attempts):
        try:
            if operation():
                return True
        except Exception:
            pass

        if attempt < max_attempts - 1:
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)

    return False
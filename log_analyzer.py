from typing import Iterable
import re

class LogAnalyzer:
    def process_logs(
        self,
        logs: Iterable[str],
        target_service: str,
        target_code: int
    ) -> float:
        total_latency = 0
        events_count = 0

        service_token = f"Service: {target_service}"
        code_token = f"Code: {target_code}"

        latency_pattern = re.compile(r"Latency:\s*(\d+)")

        for log in logs:
            if "ERROR" not in log:
                continue

            if service_token not in log:
                continue

            if code_token not in log:
                continue

            match = latency_pattern.search(log)
            if not match:
                continue

            total_latency += int(match.group(1))
            events_count += 1

        return total_latency / events_count if events_count else 0.0

            
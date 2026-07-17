import re
import heapq

def process_log_files(file_path: str, slow_threshold_ms: int = 500) -> dict:
    """
    Input sample:
        [2026-07-17T08:15:00Z] 192.168.1.1 GET /api/v1/users 200 45
        [2026-07-17T08:15:02Z] 10.0.0.5 POST /api/v1/checkout 500 1250
        [2026-07-17T08:15:03Z] 192.168.1.1 GET /api/v1/users 401 12
        [2026-07-17T08:15:04Z] MALFORMED_LINE_WITHOUT_PROPER_SPACES
        [2026-07-17T08:15:05Z] 172.16.0.2 GET /static/logo.png 200 8
    Output: 
        Total Requests: The number of successfully parsed requests.
        Error Rate: The percentage of requests that returned a $5xx$ status code (e.g., $500, 502, 503, 504$).
        Top IPs: The top 3 IP addresses with the most requests.
        Slow Endpoints: The paths (PATH) where the average response time exceeds a given threshold (say, $500$ ms), sorted from slowest to fastest.
        Corrupted Lines Count: The count of lines that failed parsing.
    """

    total_requests = 0
    corrupted_lines = 0
    total_errors = 0
    endpoints_ms = {}
    ip_counter = {}

    pattern = re.compile(
        r"^\[([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)\]\s+"
        r"([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})\s+"
        r"([A-Z]+)\s+"
        r"([^\s]+)\s+"
        r"([0-9]{3})\s+"
        r"(\d+)$"
    )

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            match = pattern.fullmatch(line)
            if not match:
                corrupted_lines += 1
                continue

            total_requests += 1
            timestamp, ip, endpoint, code, ms = match.groups()

            ms = int(ms)
            code = int(code)

            if code >= 500:
                total_errors += 1
            
            ip_counter[ip] = ip_counter.get(ip, 0) + 1
            
            if endpoint not in endpoints_ms:
                endpoints_ms[endpoint] = (ms, 1) 
            else:
                old_ms, count = endpoints_ms[endpoint] 
                endpoints_ms[endpoint] = (old_ms+ms, count+1)
        
        ips_heap = []
        for ip, count in ip_counter.items():
            heapq.heappush(ips_heap, (count, ip))
            if len(ips_heap) > 3:
                heapq.heappop(ips_heap)

        top_ips = []
        for count, ip in ips_heap:
             top_ips.append((ip, count))

        error_rate_percentage = 0
        if total_errors:
            error_rate_percentage = total_errors / total_requests * 100

        slow_endpoints = []
        for endpoint, (total_ms, count) in endpoints_ms.items():
            avg_ms = total_ms/count
            if avg_ms >= slow_threshold_ms:
                slow_endpoints.append((endpoint, avg_ms))

    slow_endpoints.sort(key=lambda x: x[1], reverse=True)
    
    return {
        "total_requests": total_requests,
        "error_rate_percentage": round(error_rate_percentage, 2), # Calculate this
        "top_ips": top_ips,                # Calculate this (list of tuples: [(ip, count), ...])
        "slow_endpoints": slow_endpoints,         # Calculate this (list of tuples: [(path, avg_ms), ...])
        "corrupted_lines": corrupted_lines
    }

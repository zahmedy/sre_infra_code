class ErrorCounter:
    def __init__(self):
        self.timestamps = [-1] * 300
        self.counts = [0] * 300

    def record(self, timestamp: int) -> None:
        index = timestamp % 300
        
        if self.timestamps[index] != timestamp:
            self.timestamps[index] = timestamp
            self.counts[index] = 0

        self.counts[index] += 1

    def count(self, timestamp: int) -> int:
        total_errors = 0
        window_start = timestamp - 299

        for index in range(300):
            stored_timestamp = self.timestamps[index]

            if  window_start <= stored_timestamp <= timestamp:
                total_errors += self.counts[index]

        return total_errors
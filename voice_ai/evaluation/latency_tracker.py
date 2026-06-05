import time


class LatencyTracker:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def get_latency(self):
        if self.start_time and self.end_time:
            return round(self.end_time - self.start_time, 3)
        return None

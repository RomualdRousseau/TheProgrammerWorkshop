import math


class Timer:
    def __init__(self, time: float):
        self.time = math.inf
        self.max_time = time

    def is_running(self):
        return self.time != math.inf

    def is_elapsed(self):
        return self.time <= 0

    def set(self):
        if not self.is_running():
            self.time = self.max_time

    def reset(self):
        if self.is_running():
            self.time = math.inf

    def update(self, dt: float):
        if self.is_running():
            self.time = max(self.time - dt, 0)

import math


class Timer:
    def __init__(self):
        self.time = math.inf

    def is_running(self):
        return self.time != math.inf

    def is_elapsed(self):
        return self.time <= 0

    def set(self, time: float):
        if not self.is_running():
            self.time = time

    def reset(self):
        if self.is_running():
            self.time = math.inf

    def update(self, dt: float):
        if self.is_running():
            self.time = max(self.time - dt, 0)

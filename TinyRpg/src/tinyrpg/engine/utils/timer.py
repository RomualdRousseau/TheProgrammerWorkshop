import math


class Timer:
    def __init__(self, time: float):
        self.time = time
        self.remain = math.inf

    def is_running(self):
        return self.remain != math.inf

    def is_elapsed(self):
        return self.remain <= 0

    def set(self):
        if not self.is_running():
            self.remain = self.time

    def reset(self):
        if self.is_running():
            self.remain = math.inf

    def update(self, dt: float):
        if self.is_running():
            self.remain = max(self.remain - dt, 0)

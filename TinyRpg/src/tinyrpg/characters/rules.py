import math
from random import uniform


class Rules:
    def get_hits(self, damage: float, armor: float) -> float:
        return max(0, damage - math.floor(uniform(0, armor + 1)))

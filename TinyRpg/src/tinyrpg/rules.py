import math
from random import uniform


def get_hits(damage: float, armor: float) -> float:
    return max(0, damage - math.floor(uniform(0, armor + 1)))

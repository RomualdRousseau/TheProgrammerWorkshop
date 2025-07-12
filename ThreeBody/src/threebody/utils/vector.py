from random import random

import pyray as pr


def vector3_random() -> pr.Vector3:
    return pr.Vector3(2 * random() - 1, 2 * random() - 1, 2 * random() - 1)

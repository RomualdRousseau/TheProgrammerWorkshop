from typing import Protocol

import pyray as pr


class Entity(Protocol):
    mass: float
    force: pr.Vector3
    rho: pr.Vector3
    pos: pr.Vector3

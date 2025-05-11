from random import random

import numpy as np
import pyray as pr
from numba import njit

from metaball import EPSILON, FIELD_HEIGHT, FIELD_WIDTH, METABALL_RADIUS, METABALL_SPEED

Metaball = tuple[float, float, int, float, float]


@njit
def field_func(metaball: Metaball, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    e_x, e_y, e_r, _, _ = metaball
    dist = (e_x - x) ** 2 + (e_y - y) ** 2
    return e_r**2 / (dist + EPSILON)


def create_metaballs(n: int) -> list[Metaball]:
    return [create_metaball() for _ in range(n)]


def update_metaballs(metaballs: list[Metaball], dt: float) -> list[Metaball]:
    return [update_metaball_physic(metaball, dt) for metaball in metaballs]


def generate_metaballs(metaballs: list[Metaball], palette: np.ndarray) -> pr.Image:
    field_x, field_y = np.indices((FIELD_HEIGHT, FIELD_WIDTH))
    field = np.sum([field_func(metaball, field_x, field_y) for metaball in metaballs], axis=0)
    hue = np.clip(255 * field, 0, 255).astype(np.uint8)
    pixels = palette[hue]
    return pr.Image(pixels, FIELD_WIDTH, FIELD_HEIGHT, 1, pr.PixelFormat.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8)


def create_metaball() -> Metaball:
    e_r = int(pr.lerp(METABALL_RADIUS, METABALL_RADIUS * 2, random()))
    e_x, e_y = pr.lerp(e_r, FIELD_WIDTH - e_r, random()), pr.lerp(e_r, FIELD_HEIGHT - e_r, random())
    e_vx, e_vy = pr.lerp(-METABALL_SPEED, METABALL_SPEED, random()), pr.lerp(-METABALL_SPEED, METABALL_SPEED, random())
    return (e_x, e_y, e_r, e_vx, e_vy)


def update_metaball_physic(metaball: Metaball, dt: float) -> Metaball:
    e_x, e_y, e_r, e_vx, e_vy = metaball
    if not (e_r < e_x < (FIELD_WIDTH - e_r)):
        e_vx = -e_vx
    if not (e_r < e_y < (FIELD_HEIGHT - e_r)):
        e_vy = -e_vy
    e_x, e_y = e_x + e_vx * dt, e_y + e_vy * dt
    e_x, e_y = min(max(e_x, e_r), FIELD_WIDTH - e_r), min(max(e_y, e_r), FIELD_HEIGHT - e_r)
    return (e_x, e_y, e_r, e_vx, e_vy)

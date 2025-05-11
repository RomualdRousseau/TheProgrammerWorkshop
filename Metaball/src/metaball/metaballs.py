from functools import cache
from random import random

import numpy as np
import pyray as pr
from numba import njit

from metaball import EPSILON, FIELD_HEIGHT, FIELD_WIDTH, METABALL_RADIUS, METABALL_SPEED

Metaball = tuple[float, float, int, float, float]


@njit
def compute_field(pos: np.ndarray, radius: np.ndarray, field: np.ndarray) -> np.ndarray:
    values = radius**2 / (np.sum((pos - field) ** 2, axis=-1) + EPSILON**2)
    return np.sum(values, axis=-1)


def create_metaballs(n: int) -> list[Metaball]:
    return [create_metaball() for _ in range(n)]


def update_metaballs(metaballs: list[Metaball], dt: float) -> list[Metaball]:
    return [update_metaball_physic(metaball, dt) for metaball in metaballs]


def generate_metaballs(metaballs: list[Metaball], palette: np.ndarray) -> pr.Image:
    n = len(metaballs)
    p = np.array([[x, y] for x, y, _, _, _ in metaballs])
    r = np.array([r for _, _, r, _, _ in metaballs])
    hue = np.clip(compute_field(p, r, generate_field(n)) * 255, 0, 255).astype(np.uint8)
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


@cache
def generate_field(n):
    field_x, field_y = np.indices((FIELD_HEIGHT, FIELD_WIDTH))
    return np.repeat(np.dstack((field_x, field_y)).reshape(-1, 2), n, axis=0).reshape(-1, n, 2)

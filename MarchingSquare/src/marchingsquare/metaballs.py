from random import random

import numpy as np
import pyray as pr
from numba import njit

Metaball = tuple[float, float, int, float, float]

FIELD_WIDTH = 64
FIELD_HEIGHT = 64
METABALL_RADIUS = 4
METABALL_SPEED = 50


def create_metaballs(n: int) -> list[Metaball]:
    return [create_metaball() for _ in range(n)]


def create_metaball() -> Metaball:
    e_r = int(pr.lerp(METABALL_RADIUS, METABALL_RADIUS * 2, random()))
    e_x, e_y = pr.lerp(e_r, FIELD_WIDTH - e_r, random()), pr.lerp(e_r, FIELD_HEIGHT - e_r, random())
    e_vx, e_vy = pr.lerp(-METABALL_SPEED, METABALL_SPEED, random()), pr.lerp(-METABALL_SPEED, METABALL_SPEED, random())
    return (e_x, e_y, e_r, e_vx, e_vy)


def update_metaballs(metaballs: list[Metaball], dt: float) -> list[Metaball]:
    return [update_metaball_physic(metaball, dt) for metaball in metaballs]


def generate_metaballs(metaballs: list[Metaball], palette: np.ndarray) -> pr.Image:
    pixels = generate_metaballs_pixels(metaballs, palette)
    return pr.Image(pixels, FIELD_WIDTH, FIELD_HEIGHT, 1, pr.PixelFormat.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8)


@njit
def update_metaball_physic(metabball: Metaball, dt: float) -> Metaball:
    e_x, e_y, e_r, e_vx, e_vy = metabball
    if not (e_r < e_x < (FIELD_WIDTH - e_r)):
        e_vx = -e_vx
    if not (e_r < e_y < (FIELD_HEIGHT - e_r)):
        e_vy = -e_vy
    e_x, e_y = e_x + e_vx * dt, e_y + e_vy * dt
    e_x, e_y = min(max(e_x, e_r), FIELD_WIDTH - e_r), min(max(e_y, e_r), FIELD_HEIGHT - e_r)
    return (e_x, e_y, e_r, e_vx, e_vy)


@njit
def generate_metaballs_pixels(metaballs: list[Metaball], palette: np.ndarray) -> np.ndarray:
    pixels = np.zeros((FIELD_HEIGHT, FIELD_WIDTH, 4), dtype=np.uint8)
    for y in range(FIELD_HEIGHT):
        for x in range(FIELD_WIDTH):
            hue = sum([function_metaball(metaball, x, y) for metaball in metaballs])
            hue = int(min(max(255 * hue, 0), 255))
            pixels[y, x] = palette[hue]
    return pixels


@njit
def function_metaball(metaball: Metaball, x: float, y: float) -> float:
    e_x, e_y, e_r, _, _ = metaball
    dist = (e_x - x) ** 2 + (e_y - y) ** 2
    return 1.0 if dist == 0.0 else e_r**2 / dist

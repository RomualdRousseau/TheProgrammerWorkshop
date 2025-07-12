from functools import cache
from random import uniform

import numpy as np
import pyray as pr
from numba import njit

from metaball import EPSILON, FIELD_HEIGHT, FIELD_WIDTH, METABALL_RADIUS, METABALL_SPEED

Metaballs = tuple[int, np.ndarray, np.ndarray, np.ndarray]


def create_metaballs(n: int) -> Metaballs:
    metaballs = [create_metaball() for _ in range(n)]
    n = len(metaballs)
    p = np.array([[x, y] for x, y, _, _, _ in metaballs])
    r = np.array([r for _, _, r, _, _ in metaballs])
    v = np.array([[vx, vy] for _, _, _, vx, vy in metaballs])
    return (n, p, r, v)


def update_metaballs(metaballs: Metaballs, dt: float) -> Metaballs:
    n, p, r, v = metaballs
    field_bbox_min, field_bbox_max = generate_field_bbox(r)
    v = np.where(p > field_bbox_min, v, -v)
    v = np.where(p < field_bbox_max, v, -v)
    p += v * dt
    p = np.clip(p, field_bbox_min, field_bbox_max)
    return (n, p, r, v)


def generate_metaballs(metaballs: Metaballs, palette: np.ndarray) -> pr.Image:
    n, p, r, _ = metaballs
    hue = compute_field(p, r, generate_field(n))
    pixels = palette[hue]
    return pr.Image(pixels, FIELD_WIDTH, FIELD_HEIGHT, 1, pr.PixelFormat.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8)


def create_metaball() -> tuple[float, float, int, float, float]:
    r = int(uniform(METABALL_RADIUS, METABALL_RADIUS * 2))
    p_x, p_y = uniform(r, FIELD_WIDTH - r), uniform(r, FIELD_HEIGHT - r)
    v_x, v_y = uniform(-METABALL_SPEED, METABALL_SPEED), uniform(-METABALL_SPEED, METABALL_SPEED)
    return (p_x, p_y, r, v_x, v_y)


@cache
def generate_field(n: int) -> np.ndarray:
    field_x, field_y = np.indices((FIELD_HEIGHT, FIELD_WIDTH))
    return np.repeat(np.dstack((field_x, field_y)).reshape(-1, 2), n, axis=0).reshape(-1, n, 2)


@njit
def generate_field_bbox(radius: np.ndarray) -> np.ndarray:
    min, max = (
        np.dstack((radius, radius)).reshape(-1, 2),
        np.dstack((FIELD_WIDTH - radius, FIELD_HEIGHT - radius)).reshape(-1, 2),
    )
    return np.stack((min, max))


@njit
def compute_field(pos: np.ndarray, radius: np.ndarray, field: np.ndarray) -> np.ndarray:
    values = radius**2 / (np.sum((pos - field) ** 2, axis=-1) + EPSILON**2)
    return np.clip(np.sum(values, axis=-1) * 255, 0, 255).astype(np.uint8)

import numpy as np
import pyray as pr

from metaball import METABALLS_COUNT, METABALLS_PALETTE, WINDOW_HEIGHT, WINDOW_WIDTH
from metaball.metaballs import (
    Metaballs,
    create_metaballs,
    generate_metaballs,
    update_metaballs,
)


class Context:
    metaballs: Metaballs
    palette: np.ndarray
    texture: pr.Texture


def init() -> None:
    Context.metaballs = create_metaballs(METABALLS_COUNT)
    Context.palette = METABALLS_PALETTE()
    image = generate_metaballs(Context.metaballs, Context.palette)
    Context.texture = pr.load_texture_from_image(image)


def release() -> None:
    pr.unload_texture(Context.texture)


def update(dt: float) -> None:
    Context.metaballs = update_metaballs(Context.metaballs, dt)


def draw() -> None:
    image = generate_metaballs(Context.metaballs, Context.palette)
    pr.update_texture(Context.texture, image.data)

    pr.draw_texture_pro(
        Context.texture,
        (0, 0, Context.texture.width, Context.texture.height),
        (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
        (0, 0),
        0,
        pr.WHITE,
    )
    pr.draw_fps(10, 10)

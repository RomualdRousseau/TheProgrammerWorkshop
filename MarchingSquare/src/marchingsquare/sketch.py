import numpy as np
import pyray as pr

from marchingsquare import WINDOW_HEIGHT, WINDOW_WIDTH
from marchingsquare.metaballs import (
    Metaball,
    create_metaballs,
    generate_metaballs,
    update_metaballs,
)
from marchingsquare.palettes import generate_fire_palette

N = 5


class Context:
    metaballs: list[Metaball]
    palette: np.ndarray
    texture: pr.Texture


def init() -> None:
    Context.metaballs = create_metaballs(N)
    Context.palette = generate_fire_palette()
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

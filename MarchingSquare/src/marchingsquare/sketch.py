import pyray as pr

from marchingsquare import WINDOW_HEIGHT, WINDOW_WIDTH
from marchingsquare.metaballs import (
    Metaball,
    create_metaballs,
    generate_metaballs,
    update_metaballs,
)

N = 5


class Context:
    metaballs: list[Metaball]
    texture: pr.Texture


def init() -> None:
    Context.metaballs = create_metaballs(N)
    image = generate_metaballs(Context.metaballs)
    Context.texture = pr.load_texture_from_image(image)


def release() -> None:
    pr.unload_texture(Context.texture)


def update(dt: float) -> None:
    Context.metaballs = update_metaballs(Context.metaballs, dt)


def draw() -> None:
    image = generate_metaballs(Context.metaballs)
    pr.update_texture(Context.texture, image.data)
    pr.draw_texture_pro(
        Context.texture,
        (0, 0, Context.texture.width, Context.texture.height),
        (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
        (0, 0),
        0,
        pr.WHITE,
    )

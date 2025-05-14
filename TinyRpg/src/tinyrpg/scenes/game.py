import pyray as pr

from tinyrpg.resources import unload_resources
from tinyrpg.sprites.hero import Hero


class Context:
    camera: pr.Camera2D
    hero: Hero


def init() -> None:
    Context.camera = pr.Camera2D((512, 512), (0, 0), 0, 4)
    Context.hero = Hero(pr.Vector2(-24, -24))


def release() -> None:
    unload_resources()


def update(dt: float) -> None:
    Context.hero.update(dt)


def draw() -> None:
    pr.clear_background(pr.RAYWHITE)
    pr.begin_mode_2d(Context.camera)
    Context.hero.draw()
    pr.end_mode_2d()
    pr.draw_fps(10, 10)

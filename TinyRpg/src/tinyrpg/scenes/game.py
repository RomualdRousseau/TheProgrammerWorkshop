import pyray as pr
from pytmx import TiledMap

from tinyrpg.utils.pyray_util import draw_tiledmap
from tinyrpg.utils.resources import load_map, unload_resources
from tinyrpg.sprites.hero import Hero


class Context:
    camera: pr.Camera2D
    hero: Hero
    map: TiledMap


def init() -> None:
    Context.camera = pr.Camera2D((512, 512), (0, 0), 0, 4)
    Context.map = load_map("level1")
    Context.hero = Hero(pr.Vector2(-24, -24))


def release() -> None:
    unload_resources()


def update(dt: float) -> None:
    Context.hero.update(dt)


def draw() -> None:
    Context.camera.target = Context.hero.pos
    pr.clear_background(pr.Color(155, 212, 195, 255))
    pr.begin_mode_2d(Context.camera)
    draw_tiledmap(Context.map, pr.Vector2(-10, -10), pr.Vector2(16, 16))
    Context.hero.draw()
    pr.end_mode_2d()
    pr.draw_fps(10, 10)

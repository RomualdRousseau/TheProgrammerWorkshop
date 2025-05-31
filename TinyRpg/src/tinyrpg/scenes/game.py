from dataclasses import dataclass
from functools import cache

import pyray as pr

from tinyrpg.resources import unload_resources
from tinyrpg.sprites.hero import Hero
from tinyrpg.utils.draw import begin_draw, end_draw
from tinyrpg.utils.tiledmap import CachedTiledMap, collide_tiledmap, draw_tiledmap, load_tiledmap


@dataclass
class Game:
    camera: pr.Camera2D
    map: CachedTiledMap
    hero: Hero

    def update(self, dt: float):
        self.hero.update(dt)
        collision_vector = pr.vector2_zero()
        collision_vector = collide_tiledmap(self.hero.get_bbox(), self.map, pr.Vector2(-10, -10), collision_vector)
        self.hero.collide(collision_vector, dt)

    def draw(self):
        self.camera.target = self.hero.pos
        pr.clear_background(pr.Color(62, 137, 72, 255))
        pr.begin_mode_2d(self.camera)

        begin_draw()
        draw_tiledmap(self.map, pr.Vector2(-10, -10))
        self.hero.draw()
        end_draw()

        pr.end_mode_2d()
        pr.draw_fps(10, 10)


@cache
def get_game(level_name: str) -> Game:
    return Game(
        pr.Camera2D((512, 512), (0, 0), 0, 4),
        load_tiledmap(level_name),
        Hero(pr.Vector2(-24, -24)),
    )


def init() -> None:
    get_game("level1")  # force game to load


def release() -> None:
    get_game.cache_clear()
    unload_resources()


def update(dt: float) -> None:
    get_game("level1").update(dt)


def draw() -> None:
    get_game("level1").draw()

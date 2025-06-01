from dataclasses import dataclass
from functools import cache

import pyray as pr

from tinyrpg.engine.map import Map
from tinyrpg.engine.particle import Particle
from tinyrpg.particles.hey import Hey
from tinyrpg.resources import load_map, load_music, unload_resources
from tinyrpg.sprites.hero import Hero
from tinyrpg.utils.draw_manager import begin_draw


@dataclass
class Game:
    camera: pr.Camera2D
    map: Map
    music: pr.Music
    hero: Hero
    particles: list[Particle]


@cache
def get_game(level_name: str) -> Game:
    return Game(
        pr.Camera2D((512, 512), (0, 0), 0, 4),
        load_map(level_name + "_map"),
        load_music(level_name + "_music"),
        Hero(pr.Vector2(0, -24)),
        [],
    )


def init() -> None:
    game = get_game("level1")
    pr.play_music_stream(game.music)


def release() -> None:
    get_game.cache_clear()
    unload_resources()


def update(dt: float) -> None:
    game = get_game("level1")
    pr.update_music_stream(game.music)
    game.hero.update(dt)
    for particle in game.particles:
        particle.update(dt)
    game.particles = [particle for particle in game.particles if particle.is_alive()]

    has_collision, collision_vector = game.map.check_collide_bbox(game.hero.get_bbox(), pr.vector2_zero())
    if has_collision:
        game.particles.append(Hey(pr.Vector2(game.hero.pos.x + 16, game.hero.pos.y - 8)))
        game.hero.collide(collision_vector, dt)


def draw() -> None:
    game = get_game("level1")
    game.camera.target = game.hero.pos
    pr.clear_background(pr.Color(62, 137, 72, 255))
    with begin_draw(game.camera):
        game.map.draw()
        game.hero.draw()
        for particle in game.particles:
            particle.draw()
    pr.draw_fps(10, 10)

from dataclasses import dataclass, field
from functools import cache
from random import random

import pyray as pr

from tinyrpg.engine.draw_manager import begin_draw
from tinyrpg.engine.map import Map
from tinyrpg.engine.particle import Particle
from tinyrpg.particles.hey import Hey
from tinyrpg.resources import load_map, load_music, unload_resources
from tinyrpg.sprites.hero import ActionSprite, Hero

WORLD_BOUNDARY = pr.BoundingBox((-32, -32), (32, 32))  # pixels


@dataclass
class Game:
    camera: pr.Camera2D
    map: Map
    music: pr.Music
    hero: Hero
    particles: list[Particle] = field(default_factory=lambda: [])


@cache
def get_game(level_name: str) -> Game:
    return Game(
        pr.Camera2D((512, 512), (0, 0), 0, 4),
        load_map(f"{level_name}_map"),
        load_music(f"{level_name}_music"),
        Hero(pr.Vector2(0, -24)),
    )


def init() -> None:
    game = get_game("level1")
    pr.play_music_stream(game.music)


def release() -> None:
    get_game.cache_clear()
    unload_resources()


def update(dt: float) -> None:
    game = get_game("level1")

    # Physic updates

    game.hero.update(dt)
    for particle in game.particles:
        particle.update(dt)

    # Collisions

    has_collision, collision_vector = game.map.check_collide_bbox(game.hero.get_bbox(), pr.vector2_zero())
    if has_collision:
        game.hero.collide(collision_vector, dt)

    # Effects

    if game.hero.action == ActionSprite.IDLING and random() < 0.0025:
        game.particles.append(Hey(pr.Vector2(game.hero.pos.x + 14, game.hero.pos.y - 6), "?"))

    if ActionSprite.COLLIDING in game.hero.action and random() < 0.05:
        game.particles.append(Hey(pr.Vector2(game.hero.pos.x + 14, game.hero.pos.y - 6), "!"))

    # Garbage collect dead objects

    game.particles = [particle for particle in game.particles if particle.is_alive()]


def draw() -> None:
    game = get_game("level1")
    pr.update_music_stream(game.music)

    # Setup camera

    game.camera.target = game.hero.pos
    game.camera.target.x = max(WORLD_BOUNDARY.min.x, min(game.camera.target.x, WORLD_BOUNDARY.max.x))
    game.camera.target.y = max(WORLD_BOUNDARY.min.y, min(game.camera.target.y, WORLD_BOUNDARY.max.y))

    # Draw all objects

    pr.clear_background(game.map.get_background_color())
    with begin_draw(game.camera):
        game.map.draw()
        game.hero.draw()
        for particle in game.particles:
            particle.draw()

    pr.draw_fps(10, 10)

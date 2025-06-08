from dataclasses import dataclass, field
from functools import cache
from random import random

import pyray as pr

from tinyrpg.constants import WINDOW_HEIGHT, WINDOW_WIDTH, WORLD_WIDTH
from tinyrpg.engine.map import Map
from tinyrpg.engine.particle import Particle
from tinyrpg.engine.renderer import begin_renderer_draw
from tinyrpg.engine.widget import Widget
from tinyrpg.particles.message import Message
from tinyrpg.particles.toast import Toast
from tinyrpg.resources import load_map, load_music, unload_resources
from tinyrpg.sprites.hero import ActionHero, Hero


@dataclass
class Game:
    camera: pr.Camera2D
    map: Map
    music: pr.Music
    hero: Hero
    particles: list[Particle] = field(default_factory=lambda: [])
    messages: list[Widget] = field(default_factory=lambda: [])


@cache
def get_game(level_name: str) -> Game:
    return Game(
        pr.Camera2D((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), (0, 0), 0, WINDOW_WIDTH // WORLD_WIDTH),
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
    for message in game.messages:
        message.update(dt)

    # Collisions

    has_collision, collision_vector = game.map.check_collide_bbox(game.hero.get_bbox(), pr.vector2_zero())
    if has_collision:
        game.hero.collide(collision_vector, dt)

    # Effects

    if game.hero.action == ActionHero.IDLING and random() < 0.0025:
        game.particles.append(Toast(pr.Vector2(game.hero.pos.x + 14, game.hero.pos.y - 6), "?"))

    if ActionHero.COLLIDING in game.hero.action and random() < 0.05:
        game.particles.append(Toast(pr.Vector2(game.hero.pos.x + 14, game.hero.pos.y - 6), "!"))

    if pr.is_key_pressed(pr.KeyboardKey.KEY_A) and game.hero.action != ActionHero.TALKING:
        game.messages.append(Message("Hero", "Hello, how are you?\nLong time no see!", game.camera))
        game.hero.start_talk()

    if len(game.messages) == 0 and game.hero.action == ActionHero.TALKING:
        game.hero.stop_talk()

    # Garbage collect dead objects

    game.particles = [particle for particle in game.particles if particle.is_alive()]
    game.messages = [message for message in game.messages if message.is_opened()]


def draw() -> None:
    game = get_game("level1")
    pr.update_music_stream(game.music)

    # Setup camera

    world_boundary = game.map.get_world_boundary()
    game.camera.target = game.hero.pos
    game.camera.target.x = max(world_boundary.min.x, min(game.camera.target.x, world_boundary.max.x))
    game.camera.target.y = max(world_boundary.min.y, min(game.camera.target.y, world_boundary.max.y))

    # Draw all objects

    pr.clear_background(game.map.get_background_color())

    with begin_renderer_draw(game.camera):
        game.map.draw()
        game.hero.draw()
        for particle in game.particles:
            particle.draw()
        for message in game.messages:
            message.draw()

    pr.draw_fps(10, 10)

import math
from dataclasses import dataclass, field
from functools import cache
from random import random

import pyray as pr

from tinyrpg.engine.camera import FixedCamera, FollowCamera
from tinyrpg.engine.map import Map
from tinyrpg.engine.particle import Particle
from tinyrpg.engine.renderer import begin_mode_sorted_2d
from tinyrpg.engine.widget import Widget
from tinyrpg.particles.toast import Toast
from tinyrpg.resources import load_map, load_music, unload_resources
from tinyrpg.sprites.hero import ActionHero, Hero
from tinyrpg.widgets.dialog import Dialog
from tinyrpg.widgets.message import Message


@dataclass
class Game:
    fixed_camera: FixedCamera
    follow_camera: FollowCamera
    map: Map
    music: pr.Music
    hero: Hero
    particles: list[Particle] = field(default_factory=lambda: [])
    messages: list[Widget] = field(default_factory=lambda: [])


@cache
def get_game(level_name: str) -> Game:
    return Game(
        FixedCamera(),
        FollowCamera(),
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

    # Setup camera

    game.follow_camera.set_boundary(game.map.get_world_boundary())
    if len(game.messages) > 0:
        game.follow_camera.boundary.max.y = math.inf
    game.follow_camera.set_follower(game.hero)
    game.follow_camera.update(dt)

    # Effects

    if game.hero.action == ActionHero.IDLING and random() < 0.0025:
        game.particles.append(Toast(pr.Vector2(game.hero.pos.x + 14, game.hero.pos.y - 4), "?"))

    if ActionHero.COLLIDING in game.hero.action and random() < 0.05:
        game.particles.append(Toast(pr.Vector2(game.hero.pos.x + 14, game.hero.pos.y - 4), "!"))

    if game.hero.action != ActionHero.TALKING and pr.is_key_pressed(pr.KeyboardKey.KEY_A):
        game.particles.append(Toast(pr.Vector2(game.hero.pos.x + 20, game.hero.pos.y - 4), "..."))
        game.messages.append(
            Dialog(
                [
                    Message(
                        "Romuald",
                        "romuald",
                        "Hello, how are you?\nI love you!",
                    ),
                    Message(
                        "Grace",
                        "grace",
                        "I am fine!\nI love you too ...",
                    ),
                ]
            )
        )
        game.hero.start_talk()

    if game.hero.action == ActionHero.TALKING and len(game.messages) == 0:
        game.hero.stop_talk()

    # Garbage collect dead objects

    game.particles = [particle for particle in game.particles if particle.is_alive()]
    game.messages = [message for message in game.messages if message.is_opened()]


def draw() -> None:
    game = get_game("level1")
    pr.update_music_stream(game.music)

    # Draw all objects

    pr.clear_background(game.map.get_background_color())

    with begin_mode_sorted_2d(game.follow_camera.camera):
        game.map.draw()
        game.hero.draw()

    pr.begin_mode_2d(game.follow_camera.camera)
    for particle in game.particles:
        particle.draw()
    pr.end_mode_2d()

    pr.begin_mode_2d(game.fixed_camera.camera)
    for message in game.messages:
        message.draw()
    pr.end_mode_2d()

    pr.draw_fps(10, 10)

import math
from dataclasses import dataclass, field
from functools import cache
from random import random

import pyray as pr

from tinyrpg.engine.camera import FixedCamera, FollowCamera
from tinyrpg.engine.map import Map
from tinyrpg.engine.particle import Particle
from tinyrpg.engine.renderer import begin_mode_sorted_2d
from tinyrpg.engine.sprite import Sprite
from tinyrpg.engine.widget import Widget
from tinyrpg.particles.toast import Toast
from tinyrpg.resources import load_map, load_music, unload_resources
from tinyrpg.sprites.hero import ActionHero, Hero
from tinyrpg.sprites.npc import Npc
from tinyrpg.widgets.dialog import DialogBox
from tinyrpg.widgets.message import MessageBox


@dataclass
class Game:
    fixed_camera: FixedCamera
    follow_camera: FollowCamera
    music: pr.Music
    map: Map
    hero: Hero
    sprites: list[Sprite] = field(default_factory=lambda: [])
    particles: list[Particle] = field(default_factory=lambda: [])
    widgets: list[Widget] = field(default_factory=lambda: [])


@cache
def get_game(level_name: str) -> Game:
    music = load_music(f"{level_name}_music")
    map = load_map(f"{level_name}_map")
    hero = Hero(map.get_start_location())
    return Game(
        FixedCamera(),
        FollowCamera(),
        music,
        map,
        hero,
    )


def init() -> None:
    game = get_game("level1")
    game.sprites.append(game.hero)
    game.sprites.append(Npc("player", game.map.triggers[0].pos))
    pr.play_music_stream(game.music)


def release() -> None:
    get_game.cache_clear()
    unload_resources()


def update(dt: float) -> None:
    game = get_game("level1")

    # Physic updates

    for entity in game.sprites + game.particles + game.widgets:
        entity.update(dt)

    # Collisions

    for entity in game.sprites:
        has_collision, collision_vector = game.map.check_collide_bbox(entity.get_bbox(), pr.vector2_zero())
        if has_collision:
            entity.collide(collision_vector, dt)

    # Gameplay and Effects

    if game.hero.action == ActionHero.IDLING and random() < 0.0025:
        game.particles.append(Toast(pr.Vector2(game.hero.pos.x + 14, game.hero.pos.y - 4), "?"))

    if ActionHero.COLLIDING in game.hero.action and random() < 0.05:
        game.particles.append(Toast(pr.Vector2(game.hero.pos.x + 14, game.hero.pos.y - 4), "!"))

    if game.hero.action != ActionHero.TALKING and game.map.check_triggers(game.hero.get_bbox()):
        game.particles.append(Toast(pr.Vector2(game.hero.pos.x + 20, game.hero.pos.y - 4), "..."))
        game.widgets.append(
            DialogBox(
                [
                    MessageBox(
                        "Romuald",
                        "romuald",
                        "Hello Grace, how are you?\nI love you!",
                    ),
                    MessageBox(
                        "Grace",
                        "grace",
                        "I am fine, Romuald!\nI love you too ...",
                    ),
                ]
            )
        )
        game.hero.start_talk()

    if game.hero.action == ActionHero.TALKING and len(game.widgets) == 0:
        game.hero.stop_talk()

    # Garbage collect dead entities

    game.particles = [particle for particle in game.particles if particle.is_alive()]
    game.widgets = [widget for widget in game.widgets if widget.is_open()]


def draw() -> None:
    game = get_game("level1")
    pr.update_music_stream(game.music)

    # Setup follow camera

    game.follow_camera.set_boundary(game.map.get_world_boundary())
    if len(game.widgets) > 0:  # Give bottom screen estate to a message box
        game.follow_camera.boundary.max.y = math.inf
    game.follow_camera.set_follower(game.hero)
    game.follow_camera.update(pr.get_frame_time())

    # Draw all objects in different layers

    pr.clear_background(game.map.get_background_color())

    with begin_mode_sorted_2d(game.follow_camera.camera):
        game.map.draw()
        for sprite in game.sprites:
            sprite.draw()

    pr.begin_mode_2d(game.follow_camera.camera)
    for particle in game.particles:
        particle.draw()
    pr.end_mode_2d()

    pr.begin_mode_2d(game.fixed_camera.camera)
    for widget in game.widgets:
        widget.draw()
    pr.end_mode_2d()

    # Display some stats

    pr.draw_fps(10, 10)

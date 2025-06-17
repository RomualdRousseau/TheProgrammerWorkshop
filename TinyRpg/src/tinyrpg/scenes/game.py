import math
from dataclasses import dataclass, field
from functools import cache
from itertools import combinations
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
from tinyrpg.sprites.enemy import ActionEnemy, Enemy
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
    hero = Hero(map.start_location)
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
    for object in game.map.objects:
        match object.type:
            case "npc":
                game.sprites.append(Npc(object.name, object.pos))
            case "enemy":
                game.sprites.append(Enemy(object.name, object.pos))
    pr.play_music_stream(game.music)


def release() -> None:
    get_game.cache_clear()
    unload_resources()


def update(dt: float) -> None:
    game = get_game("level1")

    # Physic updates

    for sprite in game.sprites + game.particles + game.widgets:
        sprite.update(dt)

    # Collisions and Triggers

    for sprite in game.sprites:
        has_collision, collision_vector = game.map.check_collide_bbox(sprite.get_bbox())
        if has_collision:
            sprite.collide(dt, collision_vector)

    for sprite, other in combinations(game.sprites, 2):
        has_collision, collision_vector = other.check_collide_bbox(sprite.get_bbox())
        if has_collision:
            sprite.collide(dt, collision_vector, other)
            other.collide(dt, pr.vector2_scale(collision_vector, -1), sprite)

    for sprite in game.sprites:
        if (
            sprite.id != "hero"
            and game.map.check_visible_points(game.hero.pos, sprite.pos)
            and sprite.actions != ActionEnemy.DYING  # type: ignore
        ):
            game.hero.visible(sprite)
            sprite.visible(game.hero)

    # AI

    if ActionHero.TALKING not in game.hero.actions:
        for sprite in game.sprites:
            sprite.think()

    # Gameplay and Effects

    if ActionHero.IDLING in game.hero.actions and random() < 0.0025:
        game.particles.append(Toast(pr.Vector2(game.hero.pos.x, game.hero.pos.y - 16), ";)"))

    if ActionHero.COLLIDING in game.hero.actions and random() < 0.05:
        game.particles.append(Toast(pr.Vector2(game.hero.pos.x, game.hero.pos.y - 16), ":("))

    for sprite in game.sprites:
        match sprite.id:
            case "hero":
                for event in sprite.events:
                    if event.name == "hit":
                        game.particles.append(Toast(pr.Vector2(sprite.pos.x, sprite.pos.y - 16), f"-{event.value}"))
            case "enemy":
                for event in sprite.events:
                    if event.name == "trigger_far_enter":
                        game.particles.append(Toast(pr.Vector2(sprite.pos.x, sprite.pos.y - 16), "!"))
                    elif event.name == "trigger_far_leave":
                        game.particles.append(Toast(pr.Vector2(sprite.pos.x, sprite.pos.y - 16), "?"))
                    elif event.name == "hit":
                        game.particles.append(Toast(pr.Vector2(sprite.pos.x, sprite.pos.y - 16), f"-{event.value}"))
            case "npc":
                for event in sprite.events:
                    if event.name == "trigger_near_enter":
                        game.particles.append(Toast(pr.Vector2(game.hero.pos.x, game.hero.pos.y - 16), "?"))
                        game.particles.append(Toast(pr.Vector2(game.sprites[1].pos.x, game.sprites[1].pos.y - 16), "!"))
                        game.widgets.append(
                            DialogBox(
                                [
                                    MessageBox(
                                        "Romuald",
                                        "portrait-player",
                                        "Hello Grace, how are you?\nI love you!",
                                    ),
                                    MessageBox(
                                        "Grace",
                                        "portrait-grace",
                                        "I am fine, Romuald!\nI love you too ...",
                                    ),
                                ]
                            )
                        )
                        game.hero.start_talk()

    # Garbage collect dead entities

    game.sprites = [sprite for sprite in game.sprites if sprite.is_alive()]
    game.particles = [particle for particle in game.particles if particle.is_alive()]
    game.widgets = [widget for widget in game.widgets if widget.is_open()]

    if game.hero.actions == ActionHero.TALKING and len(game.widgets) == 0:
        game.hero.stop_talk()


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

    pr.clear_background(game.map.background_color)

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

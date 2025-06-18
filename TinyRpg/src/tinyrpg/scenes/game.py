import math
from dataclasses import dataclass, field
from functools import cache
from itertools import combinations
from random import random

import pyray as pr

from tinyrpg.characters import Enemy, Hero, Npc
from tinyrpg.engine import (
    Character,
    CharacterAction,
    FixedCamera,
    FollowCamera,
    Map,
    Particle,
    Widget,
    begin_mode_sorted_2d,
)
from tinyrpg.particles import Toast
from tinyrpg.resources import load_map, load_music, unload_resources
from tinyrpg.widgets import DialogBox, MessageBox


@dataclass
class Game:
    fixed_camera: FixedCamera
    follow_camera: FollowCamera
    music: pr.Music
    map: Map
    hero: Hero
    characters: list[Character] = field(default_factory=lambda: [])
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
    game.characters.append(game.hero)
    for object in game.map.objects:
        match object.type:
            case "npc":
                game.characters.append(Npc(object.name, object.pos))
            case "enemy":
                game.characters.append(Enemy(object.name, object.pos))
    pr.play_music_stream(game.music)


def release() -> None:
    get_game.cache_clear()
    unload_resources()


def update(dt: float) -> None:
    game = get_game("level1")

    # Physic updates

    for character in game.characters + game.particles + game.widgets:
        character.update(dt)

    # Collisions and Triggers

    for character in game.characters:
        has_collision, collision_vector = game.map.check_collision(character.get_bbox())
        if has_collision:
            character.collide(dt, collision_vector)

    for character, other in combinations(game.characters, 2):
        has_collision, collision_vector = other.check_collision(character.get_bbox())
        if has_collision:
            character.collide(dt, collision_vector, other)
            other.collide(dt, pr.vector2_scale(collision_vector, -1), character)

        has_los = (
            character.id == "hero"
            and character.is_alive()
            and other.is_alive()
            and game.map.check_los(other.pos, character.pos)
        )
        if has_los:
            other.set_nearest_target(character)
            character.set_nearest_target(other)

    # AI

    if CharacterAction.TALKING not in game.hero.actions:
        for character in game.characters:
            character.think()

    # Gameplay and Effects

    if CharacterAction.IDLING in game.hero.actions and random() < 0.0025:
        game.particles.append(Toast(pr.Vector2(game.hero.pos.x, game.hero.pos.y - 16), ";)"))

    if CharacterAction.COLLIDING in game.hero.actions and random() < 0.05:
        game.particles.append(Toast(pr.Vector2(game.hero.pos.x, game.hero.pos.y - 16), ":("))

    for character in game.characters:
        for event in character.events:
            match (character.id, event.name):
                case ("hero", "hit"):
                    game.particles.append(Toast(pr.vector2_add(character.pos, (0, -16)), f"-{event.value}"))
                case ("skeleton", "trigger_far_enter"):
                    game.particles.append(Toast(pr.vector2_add(character.pos, (0, -16)), "!"))
                case ("skeleton", "trigger_far_leave"):
                    game.particles.append(Toast(pr.vector2_add(character.pos, (0, -16)), "?"))
                case ("skeleton", "hit"):
                    game.particles.append(Toast(pr.vector2_add(character.pos, (0, -16)), f"-{event.value}"))
                case ("grace", "trigger_near_enter"):
                    game.particles.append(Toast(pr.vector2_add(game.hero.pos, (0, -16)), "?"))
                    game.particles.append(Toast(pr.vector2_add(character.pos, (0, -16)), "!"))
                    game.widgets.append(
                        DialogBox(
                            [
                                MessageBox(
                                    "Grace",
                                    "portrait-grace",
                                    "Hello Romuald! How are you?\nHelp me to find my treasure?\nI love you ...",
                                ),
                                MessageBox(
                                    "Romuald",
                                    "portrait-player",
                                    "Hello Grace, I a good and you!\nYes, sure.\nI love you too ...",
                                ),
                            ]
                        )
                    )
                    game.hero.start_talk()

    # Garbage collect dead entities

    game.characters = [character for character in game.characters if not character.should_be_free()]
    game.particles = [particle for particle in game.particles if not particle.should_be_free()]
    game.widgets = [widget for widget in game.widgets if not widget.shoudl_be_free()]

    if game.hero.actions == CharacterAction.TALKING and len(game.widgets) == 0:
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
        for character in game.characters:
            character.draw()

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

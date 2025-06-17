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
from tinyrpg.engine.widget import Widget
from tinyrpg.particles.toast import Toast
from tinyrpg.resources import load_map, load_music, unload_resources
from tinyrpg.sprites.character import Character, CharacterAction
from tinyrpg.sprites.enemy import Enemy
from tinyrpg.sprites.hero import Hero
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
        has_collision, collision_vector = game.map.check_collide_bbox(character.get_bbox())
        if has_collision:
            character.collide(dt, collision_vector)

    for character, other in combinations(game.characters, 2):
        has_collision, collision_vector = other.check_collide_bbox(character.get_bbox())
        if has_collision:
            character.collide(dt, collision_vector, other)
            other.collide(dt, pr.vector2_scale(collision_vector, -1), character)

        has_los = (
            character.id == "hero"
            and character.is_alive()
            and other.is_alive()
            and game.map.check_los(character.pos, other.pos)
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
        match character.id:
            case "hero":
                for event in character.events:
                    if event.name == "hit":
                        game.particles.append(
                            Toast(pr.Vector2(character.pos.x, character.pos.y - 16), f"-{event.value}")
                        )
            case "skeleton":
                for event in character.events:
                    if event.name == "trigger_far_enter":
                        game.particles.append(Toast(pr.Vector2(character.pos.x, character.pos.y - 16), "!"))
                    elif event.name == "trigger_far_leave":
                        game.particles.append(Toast(pr.Vector2(character.pos.x, character.pos.y - 16), "?"))
                    elif event.name == "hit":
                        game.particles.append(
                            Toast(pr.Vector2(character.pos.x, character.pos.y - 16), f"-{event.value}")
                        )
            case "grace":
                for event in character.events:
                    if event.name == "trigger_near_enter":
                        game.particles.append(Toast(pr.Vector2(game.hero.pos.x, game.hero.pos.y - 16), "?"))
                        game.particles.append(
                            Toast(pr.Vector2(game.characters[1].pos.x, game.characters[1].pos.y - 16), "!")
                        )
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

    game.characters = [sprite for sprite in game.characters if not sprite.should_be_free()]
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
        for sprite in game.characters:
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

import math
from dataclasses import dataclass, field
from functools import cache
from itertools import combinations
from random import random
from typing import Optional

import pyray as pr

from tinyrpg.characters import Enemy, Hero, Npc
from tinyrpg.characters.hero import get_hero
from tinyrpg.constants import INPUT_OPEN_INVENTORY, INPUT_TAKE_SCREENSHOT, ITEM_DATABASE, MESSAGE_GRACE, MESSAGE_PLAYER
from tinyrpg.engine import (
    Character,
    CharacterAction,
    DialogEffect,
    FixedCamera,
    FollowCamera,
    Item,
    Map,
    Object,
    Particle,
    VerticalEffect,
    Widget,
    begin_mode_sorted_2d,
    is_action_pressed,
)
from tinyrpg.objects.chest import Chest
from tinyrpg.particles import Pick, Toast
from tinyrpg.resources import load_map, load_music, unload_resources
from tinyrpg.widgets import InventoryBox, MessageBox


@dataclass
class Game:
    fixed_camera: FixedCamera
    follow_camera: FollowCamera
    music: pr.Music
    map: Map
    hero: Hero
    characters: list[Character] = field(default_factory=lambda: [])
    objects: list[Object] = field(default_factory=lambda: [])
    particles: list[Particle] = field(default_factory=lambda: [])
    widgets: list[Widget] = field(default_factory=lambda: [])
    quest_state: int = 0
    quest_gem_to_collect: Optional[Item] = None


@cache
def get_game(level_name: str) -> Game:
    music = load_music(f"{level_name}_music")
    map = load_map(f"{level_name}_map")
    hero = get_hero()
    hero.set_position_and_boundary(map.start_location, map.get_world_boundary())
    return Game(
        FixedCamera(),
        FollowCamera(map.get_world_boundary()),
        music,
        map,
        hero,
    )


def init():
    game = get_game("level1")
    game.characters.append(game.hero)
    for object in game.map.objects:
        match object.type:
            case "npc":
                game.characters.append(Npc(object.name, object.pos, game.map.get_world_boundary()))
            case "enemy":
                game.characters.append(Enemy(object.name, object.pos, game.map.get_world_boundary()))
            case "object":
                game.objects.append(Chest(object.pos))
    pr.play_music_stream(game.music)


def release():
    get_game.cache_clear()
    unload_resources()


def update(dt: float):
    game = get_game("level1")

    if is_action_pressed(INPUT_TAKE_SCREENSHOT):
        pr.take_screenshot("screenshot.png")

    if len(game.widgets) > 0:
        update_widgets(dt)
        return

    # Physic updates

    for entity in game.characters + game.objects + game.particles:
        entity.update(dt)

    # Collisions and Triggers

    for character in game.characters:
        has_collision, collision_vector = game.map.check_collision(character.get_bbox())
        if has_collision:
            character.collide(collision_vector)

    for character, other in combinations(game.characters + game.objects, 2):
        has_collision, collision_vector = other.check_collision(character.get_bbox())
        if has_collision:
            character.collide(collision_vector, other)
            other.collide(pr.vector2_scale(collision_vector, -1), character)

    for character in game.characters:
        has_los = (
            character.id != "player"
            and game.hero.is_alive()
            and character.is_alive()
            and game.map.check_los(character.pos, game.hero.pos)
        )
        if has_los:
            game.hero.set_nearest_target(character)
            character.set_nearest_target(game.hero)

    # AI

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
                case ("player", "hit"):
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
                    game.hero.start_talk()
                    character.start_talk()

                    match game.quest_state:
                        case 0:

                            def give_sword_and_shield(game=game, character=character):
                                game.quest_state = 1
                                game.particles.append(Pick(character.pos, Item(*ITEM_DATABASE[0]), game.hero))
                                game.particles.append(Pick(character.pos, Item(*ITEM_DATABASE[1]), game.hero))

                            game.widgets.append(
                                DialogEffect(
                                    [
                                        VerticalEffect(MessageBox("Grace", "portrait-grace", MESSAGE_GRACE)),
                                        VerticalEffect(MessageBox("Romuald", "portrait-player", MESSAGE_PLAYER)),
                                    ]
                                ).on_close(give_sword_and_shield)
                            )
                        case 1:
                            game.widgets.append(
                                DialogEffect(
                                    [
                                        VerticalEffect(MessageBox("Grace", "portrait-grace", "I love you")),
                                        VerticalEffect(MessageBox("Romuald", "portrait-player", "I love you too")),
                                    ]
                                )
                            )
                        case 2:

                            def give_gift(game=game, character=character):
                                assert game.quest_gem_to_collect is not None
                                game.hero.inventory.drop(game.hero.inventory.index(game.quest_gem_to_collect))
                                game.particles.append(Pick(character.pos, Item(*ITEM_DATABASE[3]), game.hero))

                            game.widgets.append(
                                DialogEffect(
                                    [
                                        VerticalEffect(
                                            MessageBox(
                                                "Grace", "portrait-grace", "Thank you so much!\nPlease accept this gift"
                                            )
                                        ),
                                        VerticalEffect(MessageBox("Romuald", "portrait-player", "Thank you")),
                                    ]
                                ).on_close(give_gift)
                            )

    for object in game.objects:
        for event in object.events:
            match (object.id, event.name):
                case ("chest", "collide"):
                    if not object.is_open():
                        game.quest_state = 2
                        game.quest_gem_to_collect = Item(*ITEM_DATABASE[2])
                        game.particles.append(Pick(object.pos, game.quest_gem_to_collect, game.hero))
                        object.open()

    if is_action_pressed(INPUT_OPEN_INVENTORY):
        game.widgets.append(VerticalEffect(InventoryBox()))

    # Garbage collect dead entities

    game.characters = [character for character in game.characters if not character.should_be_free()]
    game.particles = [particle for particle in game.particles if not particle.should_be_free()]


def update_widgets(dt: float):
    game = get_game("level1")
    # Physic updates

    for entity in game.particles + game.widgets:
        entity.update(dt)

    # Garbage collect dead entities

    game.widgets = [widget for widget in game.widgets if not widget.should_be_free()]
    game.particles = [particle for particle in game.particles if not particle.should_be_free()]


def draw():
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
        for character in game.characters + game.objects:
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

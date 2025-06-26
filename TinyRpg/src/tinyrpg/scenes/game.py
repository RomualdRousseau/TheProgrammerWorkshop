import math
from dataclasses import dataclass, field
from functools import cache
from itertools import combinations

import pyray as pr

from tinyrpg.characters import Enemy, Hero, Npc, get_hero
from tinyrpg.constants import DEBUG_ENABLED, INPUT_OPEN_INVENTORY, INPUT_TAKE_SCREENSHOT
from tinyrpg.engine import (
    Character,
    FixedCamera,
    FollowCamera,
    Map,
    Object,
    Particle,
    VerticalEffect,
    Widget,
    begin_mode_sorted_2d,
    is_action_pressed,
)
from tinyrpg.objects import Chest
from tinyrpg.particles import PickUp, Toast
from tinyrpg.quests import GraceQuest
from tinyrpg.resources import load_map, load_music, unload_resources
from tinyrpg.widgets import InventoryBox


@dataclass
class Game:
    fixed_camera: FixedCamera
    follow_camera: FollowCamera
    music: pr.Music
    map_data: Map
    hero: Hero
    characters: list[Character] = field(default_factory=list)
    objects: list[Object] = field(default_factory=list)
    particles: list[Particle] = field(default_factory=list)
    widgets: list[Widget] = field(default_factory=list)
    quest = GraceQuest()


@cache
def get_game(level_name: str) -> Game:
    music = load_music(f"{level_name}_music")
    map_data = load_map(f"{level_name}_map")
    hero = get_hero()
    hero.set_position_and_boundary(map_data.start_location, map_data.get_world_boundary())
    return Game(
        FixedCamera(),
        FollowCamera(map_data.get_world_boundary()),
        music,
        map_data,
        hero,
    )


def init():
    game = get_game("level1")
    game.characters.append(game.hero)
    for obj in game.map_data.objects:
        match obj.type:
            case "npc":
                game.characters.append(Npc(obj.name, obj.pos, game.map_data.get_world_boundary()))
            case "enemy":
                game.characters.append(Enemy(obj.name, obj.pos, game.map_data.get_world_boundary()))
            case "object":
                game.objects.append(Chest(obj.pos))
    pr.play_music_stream(game.music)


def release():
    get_game.cache_clear()
    unload_resources()


def update_widgets(game: Game, dt: float):
    for entity in game.particles + game.widgets:
        entity.update(dt)


def update_physics(game: Game, dt: float) -> None:
    for entity in game.characters + game.objects + game.particles:
        entity.update(dt)


def update_collisions(game: Game) -> None:
    for character in game.characters:
        has_collision, collision_vector = game.map_data.check_collision(character.get_bbox())
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
            and game.map_data.check_los(character.pos, game.hero.pos)
        )
        if has_los:
            game.hero.set_nearest_target(character)
            character.set_nearest_target(game.hero)


def update_ai(game: Game) -> None:
    for character in game.characters:
        character.think()


def update_gameplay(game: Game) -> None:
    if is_action_pressed(INPUT_OPEN_INVENTORY):
        game.widgets.append(VerticalEffect(InventoryBox()))

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
                    game.hero.start_talk()
                    game.particles.append(Toast(pr.vector2_add(character.pos, (0, -16)), "!"))
                    character.start_talk()
                    game.quest.process_next_state(game)

    for obj in game.objects:
        for event in obj.events:
            match (obj.id, event.name):
                case ("chest", "collide"):
                    if not obj.is_open():
                        gem = game.quest.collect_gem()
                        game.particles.append(PickUp(game.hero.pos, pr.Vector2(0, -1), gem, game.hero))
                        obj.open()


def garbage_collect(game: Game) -> None:
    game.characters = [character for character in game.characters if not character.should_be_free()]
    game.particles = [particle for particle in game.particles if not particle.should_be_free()]
    game.widgets = [widget for widget in game.widgets if not widget.should_be_free()]


def update(dt: float):
    game = get_game("level1")

    if is_action_pressed(INPUT_TAKE_SCREENSHOT):
        pr.take_screenshot("screenshot.png")

    if game.widgets:
        update_widgets(game, dt)
    else:
        update_physics(game, dt)
        update_collisions(game)
        update_ai(game)
        update_gameplay(game)

    garbage_collect(game)


def draw():
    game = get_game("level1")
    pr.update_music_stream(game.music)

    # Setup follow camera

    game.follow_camera.set_boundary(game.map_data.get_world_boundary())
    if game.widgets:  # Give bottom screen estate to a message box
        game.follow_camera.boundary.max.y = math.inf
    game.follow_camera.set_follower(game.hero)
    game.follow_camera.update(pr.get_frame_time())

    # Draw all objects in different layers

    pr.clear_background(game.map_data.background_color)

    with begin_mode_sorted_2d(game.follow_camera.camera):
        game.map_data.draw()
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

    # Display some debug stats

    if DEBUG_ENABLED:
        pr.draw_fps(10, 10)

import math
from functools import cache
from itertools import combinations
from typing import Optional

import pyray as pr

from tinyrpg.characters import Enemy, Npc
from tinyrpg.characters.player import Player
from tinyrpg.constants import DEBUG_ENABLED, INPUT_OPEN_INVENTORY, INPUT_TAKE_SCREENSHOT
from tinyrpg.engine import (
    Character,
    FixedCamera,
    FollowCamera,
    Object,
    Particle,
    Scene,
    VerticalEffect,
    Widget,
    begin_mode_sorted_2d,
    get_inventory_item,
    is_action_pressed,
    load_map,
    load_music,
    unload_resources,
)
from tinyrpg.objects import Chest
from tinyrpg.particles import PickUp, Toast
from tinyrpg.quests.grace_quest import GraceQuest
from tinyrpg.widgets import InventoryBox


class Game:
    def __init__(self, level_name: str):
        self.level_name = level_name
        self.initialized = False

    def init(self, previous_scene: Optional[Scene] = None):
        if self.initialized:
            return

        self.map_data = load_map(f"map-{self.level_name}")
        self.music = load_music(f"music-{self.level_name}")
        self.player = Player("Romuald", self.map_data.start_location, self.map_data.get_world_boundary())
        self.fixed_camera = FixedCamera()
        self.follow_camera = FollowCamera(self.map_data.get_world_boundary())
        self.characters: list[Character] = [self.player]
        self.objects: list[Object] = []
        self.particles: list[Particle] = []
        self.widgets: list[Widget] = []

        for obj in self.map_data.objects:
            match obj.type:
                case "npc":
                    self.characters.append(Npc(obj.name, obj.pos, self.map_data.get_world_boundary()))
                case "enemy":
                    self.characters.append(Enemy(obj.name, obj.pos, self.map_data.get_world_boundary()))
                case "object":
                    self.objects.append(Chest(obj.pos))

        self.initialized = True

    def release(self):
        self.initialized = False
        unload_resources()

    def update_widgets(self, dt: float):
        for entity in self.particles + self.widgets:
            entity.update(dt)

    def update_physics(self, dt: float) -> None:
        for entity in self.characters + self.objects + self.particles:
            entity.update(dt)

    def update_collisions(self) -> None:
        for character in self.characters:
            has_collision, collision_vector = self.map_data.check_collision(character.get_bbox())
            if has_collision:
                character.collide(collision_vector)

        for character, other in combinations(self.characters + self.objects, 2):
            has_collision, collision_vector = other.check_collision(character.get_bbox())
            if has_collision:
                character.collide(collision_vector, other)
                other.collide(pr.vector2_scale(collision_vector, -1), character)

        for character in self.characters:
            has_los = (
                character.id != "player"
                and self.player.is_alive()
                and character.is_alive()
                and self.map_data.check_los(character.pos, self.player.pos)
            )
            if has_los:
                self.player.set_nearest_target(character)
                character.set_nearest_target(self.player)

    def update_ai(self) -> None:
        for character in self.characters:
            character.think()

    def update_gameplay(self) -> None:
        if is_action_pressed(INPUT_OPEN_INVENTORY):
            self.widgets.append(VerticalEffect(InventoryBox(self.player)))

        for character in self.characters:
            for event in character.events:
                match (character, event.name):
                    case Player(), "hit":
                        self.particles.append(Toast(pr.vector2_add(character.pos, (0, -16)), f"-{event.value}"))
                    case Enemy(), "trigger_far_enter":
                        self.particles.append(Toast(pr.vector2_add(character.pos, (0, -16)), "!"))
                    case Enemy(), "trigger_far_leave":
                        self.particles.append(Toast(pr.vector2_add(character.pos, (0, -16)), "?"))
                    case Enemy(), "hit":
                        self.particles.append(Toast(pr.vector2_add(character.pos, (0, -16)), f"-{event.value}"))
                    case Npc(), "trigger_near_enter":
                        self.particles.append(Toast(pr.vector2_add(self.player.pos, (0, -16)), "?"))
                        self.player.start_talk()
                        self.particles.append(Toast(pr.vector2_add(character.pos, (0, -16)), "!"))
                        character.start_talk()
                        if len(self.player.quests) == 0:
                            self.player.quests.append(GraceQuest())
                        for quest in self.player.quests:
                            quest.process_next_state(self)

        for obj in self.objects:
            for event in obj.events:
                match (obj.id, event.name):
                    case ("chest", "collide"):
                        if not obj.is_open():
                            gem = get_inventory_item("Grace_Gem")
                            self.particles.append(PickUp(self.player.pos, pr.Vector2(0, -1), gem, self.player))
                            obj.open()

    def garbage_collect(self) -> None:
        self.characters = [character for character in self.characters if not character.should_be_free()]
        self.particles = [particle for particle in self.particles if not particle.should_be_free()]
        self.widgets = [widget for widget in self.widgets if not widget.should_be_free()]

    def update(self, dt: float):
        assert self.initialized, "Game not initialized"

        if is_action_pressed(INPUT_TAKE_SCREENSHOT):
            pr.take_screenshot("screenshot.png")

        if self.widgets:
            self.update_widgets(dt)
        else:
            self.update_physics(dt)
            self.update_collisions()
            self.update_ai()
            self.update_gameplay()

        self.garbage_collect()

    def draw(self):
        assert self.initialized, "Game not initialized"

        if pr.is_music_stream_playing(self.music):
            pr.update_music_stream(self.music)
        else:
            pr.play_music_stream(self.music)

        # Setup follow camera

        self.follow_camera.set_boundary(self.map_data.get_world_boundary())
        if self.widgets:  # Give bottom screen estate to a message box
            self.follow_camera.boundary.max.y = math.inf
        self.follow_camera.set_follower(self.player)
        self.follow_camera.update(pr.get_frame_time())

        # Draw all objects in different layers

        pr.clear_background(self.map_data.background_color)

        with begin_mode_sorted_2d(self.follow_camera.camera):
            self.map_data.draw()
            for character in self.characters + self.objects:
                character.draw()

        pr.begin_mode_2d(self.follow_camera.camera)
        for particle in self.particles:
            particle.draw()
        pr.end_mode_2d()

        pr.begin_mode_2d(self.fixed_camera.camera)
        for widget in self.widgets:
            widget.draw()
        pr.end_mode_2d()

        # Display some debug stats

        if DEBUG_ENABLED:
            pr.draw_fps(10, 10)

    def get_state_and_input(self) -> tuple[str, str]:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_Q):
            return (self.level_name, "gameover")
        else:
            return (self.level_name, "self")


@cache
def get_game(level_name: str):
    return Game(level_name)

from __future__ import annotations

import io
import math
from dataclasses import dataclass
from enum import Flag, auto
from typing import Any, Optional, Protocol

import pyray as pr

from tinyrpg.constants import (
    CHARACTER_FREE_TIMER,
    CHARACTER_TRIGGER_FAR_DEFAULT,
    CHARACTER_TRIGGER_NEAR_DEFAULT,
    DEBUG_ENABLED,
)
from tinyrpg.engine.base.animation import Animation
from tinyrpg.engine.base.entity import Entity
from tinyrpg.engine.base.renderer import renderer
from tinyrpg.engine.base.resources import load_texture
from tinyrpg.engine.base.sound import play_sound
from tinyrpg.engine.base.sprite import AnimatedSprite
from tinyrpg.engine.game.inventory import Inventory
from tinyrpg.engine.utils.bbox import adjust_bbox, get_bbox_from_rect
from tinyrpg.engine.utils.pickle import DBPickler
from tinyrpg.engine.utils.timer import Timer

CHARACTER_SIZE = pr.Vector2(32, 32)  # pixels
CHARACTER_BOUNDARY_ADJUST = pr.BoundingBox((8, 0, 0), (-8, -8, 0))  # pixels
CHARACTER_BBOX_ADJUST = pr.BoundingBox((12, 20, 0), (-12, -8, 0))  # pixels
CHARACTER_DEPTH_RATIO = 0.8  # %


@dataclass
class CharacterStats:
    speed: float
    attack_speed: float
    damage: int
    armor: int
    hp: int
    xp: int = 1
    trigger_near: int = CHARACTER_TRIGGER_NEAR_DEFAULT
    trigger_far: int = CHARACTER_TRIGGER_FAR_DEFAULT


@dataclass
class CharacterEvent:
    name: str
    object: Optional[Entity]
    value: Any = None


@dataclass
class CharacterTrigger:
    dist: float = math.inf
    last: Optional[Character] = None
    curr: Optional[Character] = None


class CharacterAction(Flag):
    IDLING = auto()
    WALKING = auto()
    ATTACKING = auto()
    COLLIDING = auto()
    TALKING = auto()
    DYING = auto()


class CharacterRules(Protocol):
    def get_hits(self, damage: float, armor: float) -> float: ...


CHARACTER_NO_RESET_MASK = CharacterAction.TALKING | CharacterAction.DYING


class Character(AnimatedSprite):
    def __init__(
        self,
        id: str,
        name: str,
        pos: pr.Vector2,
        stats: CharacterStats,
        animations: dict[str, Animation],
        boundary: pr.BoundingBox,
        rules: CharacterRules,
    ):
        super().__init__(id, pos, load_texture(f"skin-{id}"), animations)
        self.name = name
        self.stats = stats
        self.health = self.stats.hp
        self.dir = pr.vector2_zero()
        self.speed = 0
        self.actions = CharacterAction.IDLING
        self.attack_timer = Timer()
        self.free_timer = Timer()
        self.trigger_near = CharacterTrigger()
        self.trigger_far = CharacterTrigger()
        self.events: list[CharacterEvent] = []
        self.boundary = adjust_bbox(boundary, CHARACTER_BOUNDARY_ADJUST)
        self.rules: CharacterRules = rules
        self.inventory: Optional[Inventory] = None

    def should_be_free(self) -> bool:
        return self.health <= 0 and self.free_timer.is_elapsed()

    def get_layer(self):
        return 1

    def get_depth(self):
        dest = self.get_dest(self.pos.x, self.pos.y)
        return dest.y + dest.height * CHARACTER_DEPTH_RATIO

    def get_bbox(self) -> pr.BoundingBox:
        rect = self.get_dest(self.pos.x, self.pos.y)
        return adjust_bbox(get_bbox_from_rect(rect), CHARACTER_BBOX_ADJUST)

    def get_damage(self):
        damage = self.stats.damage
        if self.inventory:
            for item in (i for i in self.inventory.equipment if i):
                damage += item.damage
        return damage

    def get_armor(self):
        armor = self.stats.armor
        if self.inventory:
            for item in (i for i in self.inventory.equipment if i):
                armor += item.armor
        return armor

    def is_alive(self) -> bool:
        return self.health > 0

    def set_position_and_boundary(self, pos: pr.Vector2, boundary: pr.BoundingBox):
        self.pos = pos
        self.boundary = adjust_bbox(boundary, CHARACTER_BOUNDARY_ADJUST)

    def set_nearest_target(self, other: Character):
        dist = pr.vector2_distance(self.pos, other.pos)
        if dist < self.trigger_near.dist and dist < self.stats.trigger_near:
            self.trigger_near.dist = dist
            self.trigger_near.curr = other
        if dist < self.trigger_far.dist and dist < self.stats.trigger_far:
            self.trigger_far.dist = dist
            self.trigger_far.curr = other

    def handle_ai(self):
        self.dir = pr.vector2_zero()
        self.speed = 0
        self.actions |= CharacterAction.IDLING

    def handle_attack(self):
        if self.attack_timer.is_elapsed():
            self.attack_timer.reset()
            if self.trigger_near.curr:
                self.trigger_near.curr.hit(self.get_damage())
        else:
            self.attack_timer.set(self.stats.attack_speed)

    def reset_triggers(self):
        self.trigger_near.dist = math.inf
        self.trigger_near.last = self.trigger_near.curr
        self.trigger_near.curr = None
        self.trigger_far.dist = math.inf
        self.trigger_far.last = self.trigger_far.curr
        self.trigger_far.curr = None

    def handle_triggers(self):
        if self.trigger_near.last is None and self.trigger_near.curr is not None:
            self.events.append(CharacterEvent("trigger_near_enter", self.trigger_near.curr))
        if self.trigger_near.last is not None and self.trigger_near.curr is None:
            self.events.append(CharacterEvent("trigger_near_leave", self.trigger_near.last))
        if self.trigger_near.last is not None and self.trigger_near.curr is not None:
            self.events.append(CharacterEvent("trigger_near_follow", self.trigger_near.curr))
        if self.trigger_far.last is None and self.trigger_far.curr is not None:
            self.events.append(CharacterEvent("trigger_far_enter", self.trigger_far.curr))
        if self.trigger_far.last is not None and self.trigger_far.curr is None:
            self.events.append(CharacterEvent("trigger_far_leave", self.trigger_far.last))
        if self.trigger_far.last is not None and self.trigger_far.curr is not None:
            self.events.append(CharacterEvent("trigger_far_follow", self.trigger_far.curr))

    def play_sound_effect(self) -> None:
        match self.actions:
            case a if CharacterAction.WALKING in a and int(self.animation.frame) in (1, 4):
                play_sound("step")
            case a if CharacterAction.ATTACKING in a and int(self.animation.frame) in (0, 1):
                play_sound("hit")
            case a if CharacterAction.DYING in a and int(self.animation.frame) in (0, 1):
                play_sound("hurt")

    def set_animation_effect(self) -> None:
        match self.actions:
            case a if CharacterAction.WALKING in a and self.dir.x < 0:
                self.set_animation("WalkLeft")
            case a if CharacterAction.WALKING in a and self.dir.x > 0:
                self.set_animation("WalkRight")
            case a if CharacterAction.WALKING in a and self.dir.y < 0:
                self.set_animation("WalkUp")
            case a if CharacterAction.WALKING in a and self.dir.y > 0:
                self.set_animation("WalkDown")
            case CharacterAction.ATTACKING if self.dir.x < 0:
                self.set_animation("AttackLeft")
            case CharacterAction.ATTACKING if self.dir.x > 0:
                self.set_animation("AttackRight")
            case CharacterAction.ATTACKING if self.dir.y < 0:
                self.set_animation("AttackUp")
            case CharacterAction.ATTACKING if self.dir.y > 0:
                self.set_animation("AttackDown")
            case a if CharacterAction.ATTACKING in a:
                self.set_animation("AttackDown")
            case a if CharacterAction.DYING in a:
                self.set_animation("Die")
            case _:
                self.set_animation("Idle")

    def start_talk(self):
        self.dir = pr.vector2_zero()
        self.speed = 0
        self.actions |= CharacterAction.TALKING
        self.events.clear()
        self.reset_triggers()

    def stop_talk(self):
        self.actions &= ~CharacterAction.TALKING

    def collide(self, collision_vector: pr.Vector2, other: Optional[Entity] = None):
        super().collide(collision_vector, other)
        self.actions |= CharacterAction.COLLIDING
        self.events.append(CharacterEvent("collide", other))

    def hit(self, damage: int):
        if not self.is_alive():
            return

        hits = self.rules.get_hits(damage, self.get_armor())
        if hits > 0:
            self.health -= hits
            self.events.append(CharacterEvent("hit", self, hits))

        if not self.is_alive():
            self.force = pr.vector2_zero()
            self.vel = pr.vector2_zero()
            self.dir = pr.vector2_zero()
            self.speed = 0
            self.actions = CharacterAction.DYING
            self.free_timer.set(CHARACTER_FREE_TIMER)

    def think(self):
        self.stop_talk()

        if not self.is_alive():
            return

        self.handle_triggers()
        self.handle_ai()

        if CharacterAction.ATTACKING in self.actions:
            self.handle_attack()

    def update(self, dt: float):
        if CharacterAction.TALKING in self.actions:
            return

        self.attack_timer.update(dt)
        self.free_timer.update(dt)

        self.move_constant(pr.vector2_scale(self.dir, self.speed), dt)
        self.constrain_to_boundary(self.boundary)
        super().update(dt)

        self.actions &= CHARACTER_NO_RESET_MASK
        self.events.clear()
        self.reset_triggers()

    @renderer
    def draw(self):
        self.play_sound_effect()
        self.set_animation_effect()
        super().draw()

        if DEBUG_ENABLED:
            pr.draw_bounding_box(self.get_bbox(), pr.GREEN)

    def save(self, level_name: str):
        file_data = io.BytesIO()
        DBPickler(file_data).dump(self)
        with open(f"saved/{level_name}_{self.name}.pkl", "wb") as fp:
            fp.write(file_data.getvalue())

        if self.inventory:
            self.inventory.save(self.name)

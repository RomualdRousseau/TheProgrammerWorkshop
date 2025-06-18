from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Flag, auto
from random import uniform
from typing import Any, Optional

import pyray as pr

from tinyrpg.constants import CHARACTER_FREE_TIMER, CHARACTER_TRIGGER_FAR_DEFAULT, CHARACTER_TRIGGER_NEAR_DEFAULT
from tinyrpg.engine.animation import Animation
from tinyrpg.engine.entity import Entity
from tinyrpg.engine.sprite import AnimatedSprite
from tinyrpg.engine.timer import Timer
from tinyrpg.resources import load_sound, load_texture
from tinyrpg.utils.bbox import get_bbox_from_rect

CHARACTER_WORLD_BOUNDARY = pr.BoundingBox((-168, -176), (136, 136))  # pixels
CHARACTER_BOUNDINGBOX_ADJUST = pr.BoundingBox((12, 20), (-12, -8))  # pixels
CHARACTER_DEPTH_RATIO = 0.8


@dataclass
class CharacterStats:
    speed: float
    attack_speed: float
    damage: int
    armor: int
    hp: int
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


class Character(AnimatedSprite):
    def __init__(self, name: str, pos: pr.Vector2, stats: CharacterStats, animations: dict[str, Animation]) -> None:
        super().__init__(name, pos, load_texture(name), animations)
        self.stats = stats
        self.life = self.stats.hp
        self.dir = pr.vector2_zero()
        self.speed = 0
        self.actions = CharacterAction.IDLING
        self.attack_timer = Timer()
        self.free_timer = Timer()
        self.trigger_near = CharacterTrigger()
        self.trigger_far = CharacterTrigger()
        self.events: list[CharacterEvent] = []

    def get_layer(self):
        return 1

    def get_depth(self):
        dest = self.get_dest(self.pos.x, self.pos.y)
        return dest.y + dest.height * CHARACTER_DEPTH_RATIO

    def get_bbox(self) -> pr.BoundingBox:
        bbox = get_bbox_from_rect(self.get_dest(self.pos.x, self.pos.y))
        bbox.min = pr.vector3_add(bbox.min, CHARACTER_BOUNDINGBOX_ADJUST.min)
        bbox.max = pr.vector3_add(bbox.max, CHARACTER_BOUNDINGBOX_ADJUST.max)
        return bbox

    def is_alive(self) -> bool:
        return self.life > 0

    def should_be_free(self) -> bool:
        return self.life <= 0 and self.free_timer.is_elapsed()

    def handle_ai(self):
        pass

    def handle_attack(self):
        if self.attack_timer.is_elapsed():
            self.attack_timer.reset()
            if self.trigger_near.curr:
                self.trigger_near.curr.hit(self.stats.damage)
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
            case CharacterAction.WALKING if int(self.animation.frame) in (1, 4):
                if not pr.is_sound_playing(load_sound("step")):
                    pr.play_sound(load_sound("step"))
            case CharacterAction.ATTACKING if int(self.animation.frame) in (0, 1):
                if not pr.is_sound_playing(load_sound("chop")):
                    pr.play_sound(load_sound("chop"))
            case CharacterAction.DYING if int(self.animation.frame) in (0, 1):
                if not pr.is_sound_playing(load_sound("hurt")):
                    pr.play_sound(load_sound("hurt"))

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
            case CharacterAction.ATTACKING:
                self.set_animation("AttackDown")
            case CharacterAction.DYING:
                self.set_animation("Die")
            case _:
                self.set_animation("Idle")

    def collide(self, dt: float, collision_vector: pr.Vector2, other: Optional[Entity] = None):
        super().collide(dt, collision_vector, other)
        self.actions |= CharacterAction.COLLIDING
        self.events.append(CharacterEvent("collide", other))

    def set_nearest_target(self, other: Character):
        dist = pr.vector2_distance(self.pos, other.pos)
        if dist < self.trigger_near.dist and dist < self.stats.trigger_near:
            self.trigger_near.dist = dist
            self.trigger_near.curr = other
        if dist < self.trigger_far.dist and dist < self.stats.trigger_far:
            self.trigger_far.dist = dist
            self.trigger_far.curr = other

    def hit(self, damage: int):
        damage = max(0, damage - math.floor(uniform(0, self.stats.armor + 1)))
        if damage > 0:
            self.life -= damage
            self.events.append(CharacterEvent("hit", self, damage))

    def think(self):
        if self.is_alive():
            self.handle_triggers()
            self.handle_ai()
            if CharacterAction.ATTACKING in self.actions:
                self.handle_attack()
        else:
            self.actions = CharacterAction.DYING
            self.free_timer.set(CHARACTER_FREE_TIMER)

    def update(self, dt: float):
        self.attack_timer.update(dt)
        self.free_timer.update(dt)

        self.move_constant(pr.vector2_scale(self.dir, self.speed), dt)
        self.constrain_to_world(CHARACTER_WORLD_BOUNDARY)
        super().update(dt)

        self.events.clear()
        self.reset_triggers()

    def draw(self):
        self.play_sound_effect()
        self.set_animation_effect()
        super().draw()

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Flag, auto
from typing import Any, Optional

import pyray as pr

from tinyrpg.constants import (
    DEBUG_ENABLED,
)
from tinyrpg.engine.base.animation import Animation
from tinyrpg.engine.base.entity import Entity
from tinyrpg.engine.base.renderer import BoundingBoxRenderer
from tinyrpg.engine.base.sprite import AnimatedSprite
from tinyrpg.engine.utils.bbox import adjust_bbox, get_bbox_from_rect
from tinyrpg.resources import load_sound, load_texture

OBJECT_SIZE = pr.Vector2(16, 16)  # pixels
OBJECT_BBOX_ADJUST = pr.BoundingBox((0, 0), (0, 0))  # pixels


@dataclass
class ObjectEvent:
    name: str
    object: Optional[Entity]
    value: Any = None


@dataclass
class ObjectTrigger:
    dist: float = math.inf
    last: Optional[Object] = None
    curr: Optional[Object] = None


class ObjectAction(Flag):
    IDLING = auto()
    OPENING = auto()


class Object(AnimatedSprite):
    def __init__(
        self,
        id: str,
        pos: pr.Vector2,
        animations: dict[str, Animation],
    ):
        super().__init__(id, pos, load_texture(id), animations)
        self.actions = ObjectAction.IDLING
        self.events: list[ObjectEvent] = []

    def get_layer(self):
        return 1

    def get_depth(self):
        dest = self.get_dest(self.pos.x, self.pos.y)
        return dest.y + dest.height

    def get_bbox(self) -> pr.BoundingBox:
        rect = self.get_dest(self.pos.x, self.pos.y)
        return adjust_bbox(get_bbox_from_rect(rect), OBJECT_BBOX_ADJUST)

    def open(self):
        if self.actions == ObjectAction.IDLING:
            self.actions = ObjectAction.OPENING

    def play_sound_effect(self) -> None:
        match self.actions:
            case ObjectAction.OPENING if int(self.animation.frame) == 0:
                if not pr.is_sound_playing(load_sound("hit")):
                    pr.play_sound(load_sound("hit"))

    def set_animation_effect(self) -> None:
        match self.actions:
            case ObjectAction.OPENING:
                self.set_animation("Open")
            case _:
                self.set_animation("Idle")

    def collide(self, collision_vector: pr.Vector2, other: Optional[Entity] = None):
        if self.actions == ObjectAction.IDLING:
            self.events.append(ObjectEvent("collide", other))

    def update(self, dt: float):
        super().update(dt)
        self.events.clear()

    def draw(self):
        self.play_sound_effect()
        self.set_animation_effect()
        super().draw()

        if DEBUG_ENABLED:
            BoundingBoxRenderer(self.get_bbox()).draw()

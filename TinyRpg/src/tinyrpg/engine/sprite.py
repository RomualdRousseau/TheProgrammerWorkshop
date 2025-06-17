from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Optional

import pyray as pr

from tinyrpg.constants import WORLD_FOREGROUND_LAYER
from tinyrpg.engine.animation import Animation
from tinyrpg.engine.entity import Entity
from tinyrpg.engine.renderer import renderer
from tinyrpg.utils.bbox import get_bbox_from_rect

SPRITE_TRIGGER_NEAR = 16
SPRITE_TRIGGER_FAR = 64


@dataclass
class SpriteEvent:
    name: str
    object: Optional[Entity]
    value: Any = None


@dataclass
class SpriteTrigger:
    dist: float = math.inf
    last: Optional[Sprite] = None
    curr: Optional[Sprite] = None


class Sprite(Entity):
    def __init__(self, id: str, pos: pr.Vector2, texture: pr.Texture):
        super().__init__(id, pos)
        self.texture = texture
        self.events: list[SpriteEvent] = []
        self.trigger_near = SpriteTrigger()
        self.trigger_far = SpriteTrigger()

    def get_layer(self) -> int:
        return WORLD_FOREGROUND_LAYER

    def get_depth(self) -> float:
        return self.pos.y + self.texture.height

    def get_bbox(self) -> pr.BoundingBox:
        return get_bbox_from_rect(self.get_dest(self.pos.x, self.pos.y))

    def get_dest(self, x: float, y: float) -> pr.Rectangle:
        return pr.Rectangle(
            self.pos.x - self.texture.width * 0.5,
            self.pos.y - self.texture.height * 0.5,
            self.texture.width,
            self.texture.height,
        )

    def is_alive(self) -> bool:
        return True

    def collide(self, dt: float, collision_vector: pr.Vector2, other: Optional[Entity] = None):
        super().collide(dt, collision_vector, other)
        self.events.append(SpriteEvent("collide", other))

    def visible(self, other: Sprite):
        dist = pr.vector2_distance(self.pos, other.pos)
        if dist < self.trigger_near.dist and dist < SPRITE_TRIGGER_NEAR:
            self.trigger_near.dist = dist
            self.trigger_near.curr = other
        if dist < self.trigger_far.dist and dist < SPRITE_TRIGGER_FAR:
            self.trigger_far.dist = dist
            self.trigger_far.curr = other

    def hit(self, damage: int):
        self.events.append(SpriteEvent("hit", self, damage))

    def think(self):
        if self.trigger_near.last is None and self.trigger_near.curr is not None:
            self.events.append(SpriteEvent("trigger_near_enter", self.trigger_near.curr))
        if self.trigger_near.last is not None and self.trigger_near.curr is None:
            self.events.append(SpriteEvent("trigger_near_leave", self.trigger_near.last))
        if self.trigger_near.last is not None and self.trigger_near.curr is not None:
            self.events.append(SpriteEvent("trigger_near_follow", self.trigger_near.curr))
        if self.trigger_far.last is None and self.trigger_far.curr is not None:
            self.events.append(SpriteEvent("trigger_far_enter", self.trigger_far.curr))
        if self.trigger_far.last is not None and self.trigger_far.curr is None:
            self.events.append(SpriteEvent("trigger_far_leave", self.trigger_far.last))
        if self.trigger_far.last is not None and self.trigger_far.curr is not None:
            self.events.append(SpriteEvent("trigger_far_follow", self.trigger_far.curr))

    def update(self, dt: float):
        super().update(dt)
        self.events.clear()
        self.trigger_near.dist = math.inf
        self.trigger_near.last = self.trigger_near.curr
        self.trigger_near.curr = None
        self.trigger_far.dist = math.inf
        self.trigger_far.last = self.trigger_far.curr
        self.trigger_far.curr = None

    @renderer
    def draw(self):
        pr.draw_texture_pro(
            self.texture,
            pr.Rectangle(0, 0, self.texture.width, self.texture.height),
            self.get_dest(self.pos.x, self.pos.y),
            pr.vector2_zero(),
            0.0,
            pr.WHITE,
        )


class AnimatedSprite(Sprite):
    def __init__(
        self,
        id: str,
        pos: pr.Vector2,
        texture: pr.Texture,
        animations: dict[str, Animation],
        default_name: str = "Idle",
    ):
        super().__init__(id, pos, texture)
        self.animations = animations
        self.animation = animations[default_name]

    def get_depth(self) -> float:
        dest = self.get_dest(self.pos.x, self.pos.y)
        return dest.y + dest.height

    def get_bbox(self) -> pr.BoundingBox:
        dest = self.get_dest(self.pos.x, self.pos.y)
        return get_bbox_from_rect(dest)

    def get_dest(self, x: float, y: float) -> pr.Rectangle:
        dest = self.animation.get_dest(x, y)
        dest.x -= dest.width * 0.5
        dest.y -= dest.height * 0.5
        return dest

    def set_animation(self, name: str):
        new_animation = self.animations[name]
        if self.animation != new_animation:
            self.animation = new_animation
            self.animation.frame = 0.0

    def update(self, dt: float):
        super().update(dt)
        self.animation.update(dt)

    @renderer
    def draw(self):
        pr.draw_texture_pro(
            self.texture,
            self.animation.get_source(),
            self.get_dest(self.pos.x, self.pos.y),
            self.animation.get_origin(),
            0.0,
            pr.WHITE,
        )

        # pr.draw_circle_v(self.pos, 1, pr.GREEN)
        # pr.draw_circle_lines_v(self.pos, 16, pr.GREEN)
        # pr.draw_bounding_box(self.get_bbox(), pr.GREEN)
        # pr.draw_bounding_box(get_bbox_from_rect(self.get_dest(self.pos.x, self.pos.y)), pr.GREEN)

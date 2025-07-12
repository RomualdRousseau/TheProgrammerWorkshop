from __future__ import annotations

import pyray as pr

from tinyrpg.constants import WORLD_FOREGROUND_LAYER
from tinyrpg.engine.base.animation import Animation
from tinyrpg.engine.base.entity import Entity
from tinyrpg.engine.utils.bbox import get_bbox_from_rect


class Sprite(Entity):
    def __init__(self, id: str, pos: pr.Vector2, texture: pr.Texture):
        super().__init__(id, pos)
        self.texture = texture

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

    def draw(self):
        pr.draw_texture_pro(
            self.texture,
            pr.Rectangle(0, 0, self.texture.width, self.texture.height),
            self.get_dest(self.pos.x, self.pos.y),
            pr.vector2_zero(),
            0.0,
            pr.WHITE,
        )

    # def reload_resources(self):
    #     pass


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

    def draw(self):
        pr.draw_texture_pro(
            self.texture,
            self.animation.get_source(),
            self.get_dest(self.pos.x, self.pos.y),
            self.animation.get_origin(),
            0.0,
            pr.WHITE,
        )

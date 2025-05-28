from enum import Enum

import pyray as pr

from tinyrpg.constants import EPSILON
from tinyrpg.utils.animation import Animation
from tinyrpg.utils.draw import DrawTextureCommand, emit_draw_command


class ActionSprite(Enum):
    IDLING = (0,)
    WALKING = (1,)
    ATTACKING = 2


class Sprite:
    def __init__(self, texture: pr.Texture, pos: pr.Vector2) -> None:
        self.texture = texture
        self.mass = 1.0
        self.force = pr.vector2_zero()
        self.pos = pos
        self.vel = pr.vector2_zero()

    def move_constant(self, speed: pr.Vector2, dt: float) -> None:
        mu = self.mass / (dt + EPSILON)
        friction = pr.vector2_add(pr.vector2_scale(speed, mu - 1), pr.vector2_scale(self.vel, -mu))
        self.force = pr.vector2_add(self.force, pr.vector2_add(speed, friction))

    def constrain_to_world(self, boundary: pr.Rectangle):
        self.pos.x = max(boundary.x, min(self.pos.x, boundary.x + boundary.width))
        self.pos.y = max(boundary.y, min(self.pos.y, boundary.y + boundary.height))

    def update(self, dt: float) -> None:
        acc = pr.vector2_scale(self.force, 1 / self.mass)
        self.vel = pr.vector2_add(self.vel, pr.vector2_scale(acc, dt))
        self.pos = pr.vector2_add(self.pos, pr.vector2_scale(self.vel, dt))
        self.force = pr.vector2_zero()

    def draw(self) -> None:
        source = pr.Rectangle(0, 0, self.texture.width, self.texture.height)
        dest = pr.Rectangle(self.pos.x, self.pos.y, self.texture.width, self.texture.height)
        emit_draw_command(
            DrawTextureCommand(
                5,
                0.8,
                self.texture,
                source,
                dest,
                pr.vector2_zero(),
                0.0,
            )
        )


class AnimatedSprite(Sprite):
    def __init__(
        self,
        texture: pr.Texture,
        pos: pr.Vector2,
        animations: dict[str, Animation],
        default_name: str = "Idle",
    ) -> None:
        super().__init__(texture, pos)
        self.animations = animations
        self.animation = animations[default_name]

    def set_animation(self, name: str) -> None:
        new_animation = self.animations[name]
        if self.animation != new_animation:
            self.animation = new_animation
            self.animation.frame = 0.0

    def update(self, dt: float) -> None:
        super().update(dt)
        self.animation.update(dt)

    def draw(self) -> None:
        emit_draw_command(
            DrawTextureCommand(
                4,
                0.8,
                self.texture,
                self.animation.get_source(),
                self.animation.get_dest(self.pos.x, self.pos.y),
                self.animation.get_origin(),
                0.0,
            )
        )

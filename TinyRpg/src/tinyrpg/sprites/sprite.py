import pyray as pr

from tinyrpg import EPSILON
from tinyrpg.sprites.animation import Animation


class Sprite:
    def __init__(self, texture: pr.Texture, pos: pr.Vector2) -> None:
        self.texture = texture
        self.mass = 1.0
        self.force = pr.vector2_zero()
        self.pos = pos
        self.vel = pr.vector2_zero()

    def moveConstant(self, speed: pr.Vector2, dt: float) -> None:
        mu = self.mass / (dt + EPSILON)
        friction = pr.vector2_add(
            pr.vector2_scale(speed, mu - 1), pr.vector2_scale(self.vel, -mu)
        )
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
        pr.draw_texture_v(self.texture, self.pos, pr.WHITE)


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
            self.frame = 0

    def update(self, dt: float) -> None:
        super().update(dt)
        self.animation.update(dt)

    def draw(self) -> None:
        pr.draw_texture_pro(
            self.texture,
            self.animation.get_source(),
            self.animation.get_dest(self.pos.x, self.pos.y),
            self.animation.get_origin(),
            0,
            pr.WHITE,
        )

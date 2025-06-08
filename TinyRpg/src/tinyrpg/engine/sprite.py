import pyray as pr

from tinyrpg.engine.animation import Animation
from tinyrpg.engine.entity import Entity
from tinyrpg.engine.renderer import renderer_sorted
from tinyrpg.utils.bbox import get_bbox_from_rect


class Sprite(Entity):
    def __init__(self, texture: pr.Texture, pos: pr.Vector2):
        super().__init__(pos)
        self.texture = texture

    def get_layer(self) -> int:
        return 1

    def get_depth(self) -> float:
        return self.pos.y + self.texture.height

    def get_bbox(self) -> pr.BoundingBox:
        return get_bbox_from_rect(pr.Rectangle(self.pos.x, self.pos.y, self.texture.width, self.texture.height))

    @renderer_sorted
    def draw(self):
        pr.draw_texture_pro(
            self.texture,
            pr.Rectangle(0, 0, self.texture.width, self.texture.height),
            pr.Rectangle(self.pos.x, self.pos.y, self.texture.width, self.texture.height),
            pr.vector2_zero(),
            0.0,
            pr.WHITE,
        )


class AnimatedSprite(Sprite):
    def __init__(
        self,
        texture: pr.Texture,
        pos: pr.Vector2,
        animations: dict[str, Animation],
        default_name: str = "Idle",
    ):
        super().__init__(texture, pos)
        self.animations = animations
        self.animation = animations[default_name]

    def get_layer(self) -> int:
        return 1

    def get_depth(self) -> float:
        dest = self.animation.get_dest(self.pos.x, self.pos.y)
        return dest.y + dest.height

    def get_bbox(self) -> pr.BoundingBox:
        dest = self.animation.get_dest(self.pos.x, self.pos.y)
        min = pr.Vector3(dest.x + 10, dest.y + 10, 0)
        max = pr.Vector3(dest.x + dest.width - 10 - 1, dest.y + dest.height - 10 - 1, 0)
        return pr.BoundingBox(min, max)

    def set_animation(self, name: str):
        new_animation = self.animations[name]
        if self.animation != new_animation:
            self.animation = new_animation
            self.animation.frame = 0.0

    def update(self, dt: float):
        super().update(dt)
        self.animation.update(dt)

    @renderer_sorted
    def draw(self):
        pr.draw_texture_pro(
            self.texture,
            self.animation.get_source(),
            self.animation.get_dest(self.pos.x, self.pos.y),
            self.animation.get_origin(),
            0.0,
            pr.WHITE,
        )

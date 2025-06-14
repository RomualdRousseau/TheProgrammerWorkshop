import pyray as pr

from tinyrpg.constants import WORLD_FOREGROUND_LAYER
from tinyrpg.engine.animation import Animation
from tinyrpg.engine.entity import Entity
from tinyrpg.engine.renderer import renderer
from tinyrpg.utils.bbox import get_bbox_from_rect


class Sprite(Entity):
    def __init__(self, texture: pr.Texture, pos: pr.Vector2):
        super().__init__(pos)
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
        texture: pr.Texture,
        pos: pr.Vector2,
        animations: dict[str, Animation],
        default_name: str = "Idle",
    ):
        super().__init__(texture, pos)
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

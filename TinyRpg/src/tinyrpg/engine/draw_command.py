import pyray as pr

from tinyrpg.constants import DIR8
from tinyrpg.engine.draw_manager import DrawCommand


class DrawText(DrawCommand):
    def __init__(self, layer: int, text: str, pos: pr.Vector2, fg_color: pr.Color, bg_color: pr.Color):
        super().__init__(layer, pos.y + 10)
        self.pos = pos
        self.text = text
        self.fg_color = fg_color
        self.bg_color = bg_color

    def __call__(self):
        for dir in DIR8:
            pr.draw_text(self.text, int(self.pos.x + dir[0]), int(self.pos.y + dir[1]), 10, self.bg_color)
        pr.draw_text(self.text, int(self.pos.x), int(self.pos.y), 10, self.fg_color)


class DrawRectangle(DrawCommand):
    def __init__(self, layer: int, depth_ratio: float, rect: pr.Rectangle, color: pr.Color):
        super().__init__(layer, rect.y + rect.height * depth_ratio)
        self.rect = rect
        self.color = color

    def __call__(self):
        pr.draw_rectangle_rec(self.rect, self.color)


class DrawBoundingBox(DrawCommand):
    def __init__(self, bbox: pr.BoundingBox, color: pr.Color):
        super().__init__(99, 0)
        self.bbox = bbox
        self.color = color

    def __call__(self):
        pr.draw_bounding_box(self.bbox, self.color)


class DrawTextureCommand(DrawCommand):
    def __init__(
        self,
        layer: int,
        depth_ratio: float,
        texture: pr.Texture,
        source: pr.Rectangle,
        dest: pr.Rectangle,
        origin: pr.Vector2,
        rotation: float,
    ):
        super().__init__(layer, dest.y + dest.height * depth_ratio)
        self.texture = texture
        self.source = source
        self.dest = dest
        self.origin = origin
        self.rotation = rotation

    def __call__(self):
        pr.draw_texture_pro(
            self.texture,
            self.source,
            self.dest,
            self.origin,
            self.rotation,
            pr.WHITE,
        )

import pyray as pr

from tinyrpg.constants import DIR8
from tinyrpg.engine.draw_manager import DrawCommand


class DrawText(DrawCommand):
    def __init__(self, layer: int, text: str, pos: pr.Vector2, fg_color: pr.Color, bg_color: pr.Color):
        super().__init__(layer, 0)
        self.pos = pos
        self.text = text
        self.font_size = 10
        self.fg_color = fg_color
        self.bg_color = bg_color

    def __call__(self):
        for dir in DIR8:
            pr.draw_text(self.text, int(self.pos.x + dir[0]), int(self.pos.y + dir[1]), self.font_size, self.bg_color)
        pr.draw_text(self.text, int(self.pos.x), int(self.pos.y), self.font_size, self.fg_color)


class DrawRectangle(DrawCommand):
    def __init__(self, layer: int, rect: pr.Rectangle, fg_color: pr.Color, bg_color: pr.Color):
        super().__init__(layer, 0)
        self.rect = rect
        self.fg_color = fg_color
        self.bg_color = bg_color

    def __call__(self):
        pr.draw_rectangle_rec(self.rect, self.bg_color)
        pr.draw_rectangle_lines_ex(self.rect, 2, self.fg_color)


class DrawMessage(DrawRectangle):
    def __init__(self, layer: int, text: str, pos: pr.Vector2, fg_color: pr.Color, bg_color: pr.Color):
        self.pos = pos
        self.text = text
        self.font_size = 10

        size = pr.measure_text(self.text, self.font_size)
        super().__init__(
            layer, pr.Rectangle(self.pos.x - 4, self.pos.y - 4, size + 8, self.font_size + 8), fg_color, bg_color
        )

    def __call__(self):
        super().__call__()
        pr.draw_text(self.text, int(self.pos.x), int(self.pos.y), self.font_size, self.fg_color)


class DrawBoundingBox(DrawCommand):
    def __init__(self, layer: int, bbox: pr.BoundingBox, color: pr.Color):
        super().__init__(layer, 0)
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

from typing import Optional

import pyray as pr

from tinyrpg.engine.gui.component import Component


class ImageBox(Component):
    def __init__(self, texture: pr.Texture, source: Optional[pr.Rectangle] = None):
        super().__init__()
        self.texture = texture
        if source:
            self.source = source
        else:
            self.source = pr.Rectangle(0, 0, texture.width, texture.height)

    def get_inner_rect(self) -> pr.Rectangle:
        return self.get_rect()

    def draw(self):
        inner_rect = self.get_inner_rect()

        if inner_rect.width > inner_rect.height:
            ratio = self.source.height / self.source.width
            width = inner_rect.height / ratio
            height = inner_rect.height
        elif inner_rect.width < inner_rect.height:
            ratio = self.source.width / self.source.height
            width = inner_rect.width
            height = inner_rect.width / ratio
        else:
            width = inner_rect.width
            height = inner_rect.height

        pos = pr.Vector2(
            inner_rect.x + (inner_rect.width - width) / 2,
            inner_rect.y + (inner_rect.height - height) / 2,
        )

        pr.draw_texture_pro(
            self.texture,
            self.source,
            (pos.x, pos.y, width, height),
            pr.vector2_zero(),
            0.0,
            pr.WHITE,
        )

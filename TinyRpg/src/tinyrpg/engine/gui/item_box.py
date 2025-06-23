from typing import Optional

import pyray as pr

from tinyrpg.engine.game.inventory import Item
from tinyrpg.engine.gui.component import COMPONENT_BORDER, Component
from tinyrpg.resources import load_texture


class ItemBox(Component):
    def __init__(self, item: Optional[Item] = None):
        super().__init__()
        self.item = item
        self.selected = False

    def draw(self):
        if self.selected:
            pr.draw_rectangle_lines_ex(self.get_rect(), COMPONENT_BORDER, pr.YELLOW)
        else:
            pr.draw_rectangle_lines_ex(self.get_rect(), COMPONENT_BORDER, pr.RAYWHITE)

        if self.item:
            texture = load_texture(self.item.texture)
            source = pr.Rectangle(0, 0, texture.width, texture.height)
            inner_rect = self.get_inner_rect()

            if inner_rect.width > inner_rect.height:
                ratio = source.height / source.width
                width = inner_rect.height / ratio
                height = inner_rect.height
            elif inner_rect.width < inner_rect.height:
                ratio = source.width / source.height
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
                texture,
                source,
                (pos.x, pos.y, width, height),
                pr.vector2_zero(),
                0.0,
                pr.WHITE,
            )

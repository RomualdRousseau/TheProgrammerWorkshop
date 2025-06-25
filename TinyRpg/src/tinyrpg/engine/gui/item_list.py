from typing import Optional

import pyray as pr

from tinyrpg.engine.game.inventory import Item
from tinyrpg.engine.gui.component import Component
from tinyrpg.engine.gui.text_box import TEXTBOX_COLOR_DEFAULT, TEXTBOX_FONT_SIZE_DEFAULT, TextBoxAlign
from tinyrpg.resources import load_texture

ITEMLIST_BORDER = 2  # px
ITEMLIST_BORDER_SEL = 7  # px


class ItemList(Component):
    def __init__(
        self,
        item: Optional[Item] = None,
        font_size: int = TEXTBOX_FONT_SIZE_DEFAULT,
        font_color: pr.Color = TEXTBOX_COLOR_DEFAULT,
        align: TextBoxAlign = TextBoxAlign.LEFT,
    ):
        super().__init__()
        self.item = item
        self.font_size = font_size
        self.font_color = font_color
        self.align = align
        self.selected = False
        self.texture = load_texture("gui")
        self.textureNPatch = pr.NPatchInfo(
            pr.Rectangle(0, 32, 32, 32),
            ITEMLIST_BORDER,
            ITEMLIST_BORDER,
            ITEMLIST_BORDER,
            ITEMLIST_BORDER,
            pr.NPatchLayout.NPATCH_NINE_PATCH,
        )
        self.textureNPatchSel = pr.NPatchInfo(
            pr.Rectangle(32, 32, 32, 32),
            ITEMLIST_BORDER_SEL,
            ITEMLIST_BORDER_SEL,
            ITEMLIST_BORDER_SEL,
            ITEMLIST_BORDER_SEL,
            pr.NPatchLayout.NPATCH_NINE_PATCH,
        )

    def draw(self):
        pr.draw_texture_n_patch(self.texture, self.textureNPatch, self.get_rect(), (0, 0), 0, pr.WHITE)

        if self.item:
            inner_rect = self.get_inner_rect()
            text = f"{self.item.name}\n{self.item.description}\nCost: {self.item.cost}"
            text_width = pr.measure_text(text, 10)
            match self.align:
                case TextBoxAlign.LEFT:
                    pr.draw_text(text, int(inner_rect.x), int(inner_rect.y), self.font_size, self.font_color)
                case TextBoxAlign.CENTER:
                    pr.draw_text(
                        text,
                        int(inner_rect.x + (inner_rect.width - text_width) / 2),
                        int(inner_rect.y),
                        self.font_size,
                        self.font_color,
                    )
                case TextBoxAlign.RIGHT:
                    pr.draw_text(
                        text,
                        int(inner_rect.x + inner_rect.width - text_width),
                        int(inner_rect.y),
                        self.font_size,
                        self.font_color,
                    )

        if self.selected:
            pr.draw_texture_n_patch(self.texture, self.textureNPatchSel, self.get_rect(), (0, 0), 0, pr.WHITE)

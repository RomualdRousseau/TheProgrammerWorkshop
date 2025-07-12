import pyray as pr

from tinyrpg.engine.base.resources import load_texture
from tinyrpg.engine.gui.component import Component
from tinyrpg.engine.gui.text_box import TEXTBOX_COLOR_DEFAULT, TEXTBOX_FONT_SIZE_DEFAULT, TextBoxAlign

ITEMTEXT_BORDER = 2  # px
ITEMTEXT_BORDER_SEL = 7  # px


class ItemText(Component):
    def __init__(
        self,
        text: str,
        font_size: int = TEXTBOX_FONT_SIZE_DEFAULT,
        font_color: pr.Color = TEXTBOX_COLOR_DEFAULT,
        align: TextBoxAlign = TextBoxAlign.LEFT,
    ):
        super().__init__()
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.align = align
        self.selected = False
        self.texture = load_texture("skin-gui")
        self.textureNPatch = pr.NPatchInfo(
            pr.Rectangle(0, 32, 32, 32),
            ITEMTEXT_BORDER,
            ITEMTEXT_BORDER,
            ITEMTEXT_BORDER,
            ITEMTEXT_BORDER,
            pr.NPatchLayout.NPATCH_NINE_PATCH,
        )
        self.textureNPatchSel = pr.NPatchInfo(
            pr.Rectangle(32, 32, 32, 32),
            ITEMTEXT_BORDER_SEL,
            ITEMTEXT_BORDER_SEL,
            ITEMTEXT_BORDER_SEL,
            ITEMTEXT_BORDER_SEL,
            pr.NPatchLayout.NPATCH_NINE_PATCH,
        )

    def draw(self):
        pr.draw_texture_n_patch(self.texture, self.textureNPatch, self.get_rect(), (0, 0), 0, pr.WHITE)

        inner_rect = self.get_inner_rect()
        text_width = pr.measure_text(self.text, 10)
        text_y = int(inner_rect.y + inner_rect.height / 2 - self.font_size / 2)
        match self.align:
            case TextBoxAlign.LEFT:
                pr.draw_text(self.text, int(inner_rect.x), text_y, self.font_size, self.font_color)
            case TextBoxAlign.CENTER:
                pr.draw_text(
                    self.text,
                    int(inner_rect.x + (inner_rect.width - text_width) / 2),
                    text_y,
                    self.font_size,
                    self.font_color,
                )
            case TextBoxAlign.RIGHT:
                pr.draw_text(
                    self.text,
                    int(inner_rect.x + inner_rect.width - text_width),
                    text_y,
                    self.font_size,
                    self.font_color,
                )

        if self.selected:
            pr.draw_texture_n_patch(self.texture, self.textureNPatchSel, self.get_rect(), (0, 0), 0, pr.WHITE)

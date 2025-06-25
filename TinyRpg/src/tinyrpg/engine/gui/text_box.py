from enum import Enum, auto

import pyray as pr

from tinyrpg.engine.gui.component import Component

TEXTBOX_FONT_SIZE_DEFAULT = 8  # px
TEXTBOX_COLOR_DEFAULT = pr.RAYWHITE


class TextBoxAlign(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


class TextBox(Component):
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

    def get_inner_rect(self) -> pr.Rectangle:
        return self.get_rect()

    def draw(self):
        inner_rect = self.get_inner_rect()
        text_width = pr.measure_text(self.text, 10)
        match self.align:
            case TextBoxAlign.LEFT:
                pr.draw_text(self.text, int(inner_rect.x), int(inner_rect.y), self.font_size, self.font_color)
            case TextBoxAlign.CENTER:
                pr.draw_text(
                    self.text,
                    int(inner_rect.x + (inner_rect.width - text_width) / 2),
                    int(inner_rect.y),
                    self.font_size,
                    self.font_color,
                )
            case TextBoxAlign.RIGHT:
                pr.draw_text(
                    self.text,
                    int(inner_rect.x + inner_rect.width - text_width),
                    int(inner_rect.y),
                    self.font_size,
                    self.font_color,
                )

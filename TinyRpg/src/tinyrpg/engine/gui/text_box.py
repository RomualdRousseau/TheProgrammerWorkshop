from enum import Enum, auto

import pyray as pr

from tinyrpg.engine.gui.component import Component

TEXTBOX_FONT_SIZE_DEFAULT = 8  # px


class TextBoxAlign(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


class TextBox(Component):
    def __init__(self, text: str, font_size: int = TEXTBOX_FONT_SIZE_DEFAULT, align: TextBoxAlign = TextBoxAlign.LEFT):
        super().__init__()
        self.text = text
        self.font_size = font_size
        self.align = align

    def get_inner_rect(self) -> pr.Rectangle:
        return self.get_rect()

    def draw(self):
        rect = self.get_inner_rect()
        match self.align:
            case TextBoxAlign.LEFT:
                pr.draw_text(self.text, int(rect.x), int(rect.y), self.font_size, pr.RAYWHITE)
            case TextBoxAlign.CENTER:
                text_width = pr.measure_text(self.text, 10)
                pr.draw_text(
                    self.text, int(rect.x + (rect.width - text_width) / 2), int(rect.y), self.font_size, pr.RAYWHITE
                )
            case TextBoxAlign.RIGHT:
                text_width = pr.measure_text(self.text, 10)
                pr.draw_text(self.text, int(rect.x + rect.width - text_width), int(rect.y), self.font_size, pr.RAYWHITE)

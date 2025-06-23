from __future__ import annotations

from enum import Enum, auto
from typing import Optional

import pyray as pr

from tinyrpg.constants import WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine.base.widget import Widget

WINDOW_MARGIN = 5  # px
WINDOW_PADDING = 2  # px
WINDOW_BORDER = 1  # px
WINDOW_TITLE_FONT_SIZE = 10  # px


class WindowLocation(Enum):
    TOP = auto()
    MIDDLE = auto()
    BOTTOM = auto()


class Window(Widget):
    def __init__(self, height: int, location: WindowLocation):
        pos = pr.Vector2(WINDOW_MARGIN, 0)
        size = pr.Vector2(WORLD_WIDTH - 2 * WINDOW_MARGIN, min(height, WORLD_HEIGHT - 2 * WINDOW_MARGIN))
        match location:
            case WindowLocation.TOP:
                pos.y = WINDOW_MARGIN
            case WindowLocation.MIDDLE:
                pos.y = (WORLD_HEIGHT - height) // 2
            case WindowLocation.BOTTOM:
                pos.y = WORLD_HEIGHT - WINDOW_MARGIN - height

        super().__init__(pos, size)
        self.title: Optional[str] = None
        self.widget: Optional[Widget] = None

    def get_inner_rect(self) -> pr.Rectangle:
        inner_rect = self.get_rect()
        inner_rect.x += WINDOW_PADDING
        inner_rect.y += WINDOW_PADDING
        inner_rect.width -= 2 * WINDOW_PADDING
        inner_rect.height -= 2 * WINDOW_PADDING
        return inner_rect

    def add(self, widget: Widget) -> Window:
        self.widget = widget
        return self

    def pack(self):
        rect = self.get_rect()
        pos = pr.Vector2(rect.x, rect.y)
        size = pr.Vector2(rect.width, rect.height)
        self.resize(pos, size)

    def resize(self, pos: pr.Vector2, size: pr.Vector2):
        super().resize(pos, size)
        inner_rect = self.get_inner_rect()
        if self.widget:
            pos = pr.Vector2(inner_rect.x, inner_rect.y)
            size = pr.Vector2(inner_rect.width, inner_rect.height)
            self.widget.resize(pos, size)

    def draw(self):
        rect = self.get_rect()

        if self.title:
            title_width = pr.measure_text(self.title, WINDOW_TITLE_FONT_SIZE)
            pr.draw_rectangle_v(
                (rect.x, rect.y - WINDOW_TITLE_FONT_SIZE - 1),
                (title_width + WINDOW_PADDING * 3, WINDOW_TITLE_FONT_SIZE + 1),
                pr.RAYWHITE,
            )
            pr.draw_text(
                self.title,
                int(rect.x + WINDOW_PADDING),
                int(rect.y - WINDOW_TITLE_FONT_SIZE),
                WINDOW_TITLE_FONT_SIZE,
                pr.BLUE,
            )

        pr.draw_rectangle_rec(rect, pr.color_alpha(pr.BLUE, 0.8))
        pr.draw_rectangle_lines_ex(rect, WINDOW_BORDER, pr.RAYWHITE)

        if self.widget:
            self.widget.draw()

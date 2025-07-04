from __future__ import annotations

from enum import Enum, auto
from typing import Optional

import pyray as pr

from tinyrpg.constants import WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine.base.resources import load_texture
from tinyrpg.engine.base.widget import Widget

WINDOW_MARGIN = 5  # px
WINDOW_PADDING = -1  # px
WINDOW_BORDER = 11  # px
WINDOW_TITLE_FONT_SIZE = 8  # px
WINDOW_TITLE_BORDER = 7  # px


class WindowLocation(Enum):
    TOP = auto()
    MIDDLE = auto()
    BOTTOM = auto()


class TitlePosition(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


class Window(Widget):
    def __init__(
        self,
        width: int,
        height: int,
        location: WindowLocation,
        title: Optional[str] = None,
        title_position: TitlePosition = TitlePosition.CENTER,
    ):
        pos = pr.Vector2(0, 0)
        size = pr.Vector2(min(width, WORLD_WIDTH - 2 * WINDOW_MARGIN), min(height, WORLD_HEIGHT - 2 * WINDOW_MARGIN))
        pos.x = (WORLD_WIDTH - size.x) // 2
        match location:
            case WindowLocation.TOP:
                pos.y = WINDOW_MARGIN
            case WindowLocation.MIDDLE:
                pos.y = (WORLD_HEIGHT - size.y) // 2
            case WindowLocation.BOTTOM:
                pos.y = WORLD_HEIGHT - WINDOW_MARGIN - size.y

        super().__init__(pos, size)
        self.title = title
        self.title_position = title_position
        self.widget: Optional[Widget] = None
        self.texture = load_texture("skin-gui")
        self.nPatchWindow = pr.NPatchInfo(
            pr.Rectangle(0, 0, 32, 32),
            WINDOW_BORDER,
            WINDOW_BORDER,
            WINDOW_BORDER,
            WINDOW_BORDER,
            pr.NPatchLayout.NPATCH_NINE_PATCH,
        )
        self.nPatchTitle = pr.NPatchInfo(
            pr.Rectangle(0, 64, 64, 16),
            7,
            4,
            7,
            4,
            pr.NPatchLayout.NPATCH_THREE_PATCH_HORIZONTAL,
        )

    def get_inner_rect(self) -> pr.Rectangle:
        inner_rect = self.get_rect()
        inner_rect.x += WINDOW_BORDER + WINDOW_PADDING
        inner_rect.y += WINDOW_BORDER + WINDOW_PADDING
        inner_rect.width -= 2 * (WINDOW_BORDER + WINDOW_PADDING)
        inner_rect.height -= 2 * (WINDOW_BORDER + WINDOW_PADDING)
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

        pr.draw_texture_n_patch(self.texture, self.nPatchWindow, rect, (0, 0), 0, pr.WHITE)

        if self.title:
            title_width = pr.measure_text(self.title, WINDOW_TITLE_FONT_SIZE)
            match self.title_position:
                case TitlePosition.LEFT:
                    offset = 0
                case TitlePosition.CENTER:
                    offset = (rect.width - title_width - WINDOW_TITLE_BORDER * 2) / 2
                case TitlePosition.RIGHT:
                    offset = rect.width - title_width + WINDOW_TITLE_BORDER * 2
            pr.draw_texture_n_patch(
                self.texture,
                self.nPatchTitle,
                (rect.x + offset, rect.y - WINDOW_TITLE_FONT_SIZE / 2, title_width + WINDOW_TITLE_BORDER * 2, 16),
                (0, 0),
                0,
                pr.WHITE,
            )
            pr.draw_text(
                self.title,
                int(rect.x + offset + WINDOW_TITLE_BORDER),
                int(rect.y - (WINDOW_TITLE_FONT_SIZE / 2 - 3)),
                WINDOW_TITLE_FONT_SIZE,
                pr.WHITE,
            )

        if self.widget:
            self.widget.draw()

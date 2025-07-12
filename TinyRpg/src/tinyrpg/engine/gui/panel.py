from __future__ import annotations

from typing import Optional

import pyray as pr

from tinyrpg.engine.base.resources import load_texture
from tinyrpg.engine.base.widget import Widget

PANEL_MARGIN = 1  # px
PANEL_PADDING = -1  # px
PANEL_BORDER = 7  # px


class Panel(Widget):
    def __init__(self):
        super().__init__(pr.vector2_zero(), pr.vector2_one())
        self.widget: Optional[Widget] = None
        self.texture = load_texture("skin-gui")
        self.textureNPatch = pr.NPatchInfo(
            pr.Rectangle(32, 0, 32, 32),
            PANEL_BORDER,
            PANEL_BORDER,
            PANEL_BORDER,
            PANEL_BORDER,
            pr.NPatchLayout.NPATCH_NINE_PATCH,
        )

    def get_rect(self) -> pr.Rectangle:
        rect = super().get_rect()
        rect.x += PANEL_MARGIN
        rect.y += PANEL_MARGIN
        rect.width -= 2 * PANEL_MARGIN
        rect.height -= 2 * PANEL_MARGIN
        return rect

    def get_inner_rect(self) -> pr.Rectangle:
        inner_rect = self.get_rect()
        inner_rect.x += PANEL_BORDER + PANEL_PADDING
        inner_rect.y += PANEL_BORDER + PANEL_PADDING
        inner_rect.width -= 2 * (PANEL_BORDER + PANEL_PADDING)
        inner_rect.height -= 2 * (PANEL_BORDER + PANEL_PADDING)
        return inner_rect

    def add(self, widget: Widget) -> Panel:
        self.widget = widget
        return self

    def resize(self, pos: pr.Vector2, size: pr.Vector2):
        super().resize(pos, size)
        inner_rect = self.get_inner_rect()
        if self.widget:
            pos = pr.Vector2(inner_rect.x, inner_rect.y)
            size = pr.Vector2(inner_rect.width, inner_rect.height)
            self.widget.resize(pos, size)

    def draw(self):
        pr.draw_texture_n_patch(self.texture, self.textureNPatch, self.get_rect(), (0, 0), 0, pr.WHITE)

        if self.widget:
            self.widget.draw()

from __future__ import annotations

from typing import Callable, Optional

import pyray as pr

from tinyrpg.engine.base.entity import Entity


class Widget(Entity):
    def __init__(self, pos: pr.Vector2, size: pr.Vector2):
        super().__init__("widget", pos)
        self.size = size
        self.closed = False
        self.on_close_cb: Optional[Callable[[], None]] = None
        self.on_resize_cb: Optional[Callable[[], None]] = None
        self.fixed_width = 0
        self.fixed_height = 0

    def should_be_free(self) -> bool:
        return self.closed

    def get_rect(self) -> pr.Rectangle:
        return pr.Rectangle(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def set_fixed_width(self, fixed_width: float) -> Widget:
        self.fixed_width = fixed_width
        return self

    def set_fixed_height(self, fixed_height: float) -> Widget:
        self.fixed_height = fixed_height
        return self

    def close(self):
        self.closed = True
        if self.on_close_cb:
            self.on_close_cb()

    def on_close(self, callback: Callable[[], None]) -> Widget:
        self.on_close_cb = callback
        return self

    def resize(self, pos: pr.Vector2, size: pr.Vector2):
        self.pos = pos
        self.size.x = size.x if self.fixed_width == 0 else self.fixed_width
        self.size.y = size.y if self.fixed_height == 0 else self.fixed_height
        if self.on_resize_cb:
            self.on_resize_cb()

    def on_resize(self, callback: Callable[[], None]) -> Widget:
        self.on_resize_cb = callback
        return self

    def draw(self):
        pr.draw_rectangle_lines_ex(self.get_rect(), 1, pr.GREEN)

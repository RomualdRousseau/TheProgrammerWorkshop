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

    def get_rect(self) -> pr.Rectangle:
        return pr.Rectangle(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def should_be_free(self) -> bool:
        return self.closed

    def close(self):
        self.closed = True
        if self.on_close_cb:
            self.on_close_cb()

    def on_close(self, callback: Callable[[], None]) -> Widget:
        self.on_close_cb = callback
        return self

    def draw(self):
        pr.draw_rectangle_rec(self.get_rect(), pr.GREEN)

import pyray as pr

from tinyrpg.engine.entity import Entity


class Widget(Entity):
    def __init__(self, pos: pr.Vector2, size: pr.Vector2):
        super().__init__("widget", pos)
        self.size = size
        self.closed = False

    def shoudl_be_free(self) -> bool:
        return self.closed

    def close(self):
        self.closed = True

    def get_rect(self) -> pr.Rectangle:
        return pr.Rectangle(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def draw(self):
        pr.draw_rectangle_rec(self.get_rect(), pr.GREEN)

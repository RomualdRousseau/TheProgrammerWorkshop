import pyray as pr

from tinyrpg.engine.entity import Entity


class Widget(Entity):
    def __init__(self, pos: pr.Vector2, size: pr.Vector2):
        super().__init__(pos)
        self.size = size
        self.closed = False

    def is_open(self) -> bool:
        return not self.closed

    def is_closed(self) -> bool:
        return self.closed

    def close(self):
        self.closed = True

    def get_rect(self) -> pr.Rectangle:
        return pr.Rectangle(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def get_rect_2d(self, camera: pr.Camera2D) -> pr.Rectangle:
        pos = pr.get_screen_to_world_2d((self.pos.x * camera.zoom, self.pos.y * camera.zoom), camera)
        return pr.Rectangle(pos.x, pos.y, self.size.x, self.size.y)

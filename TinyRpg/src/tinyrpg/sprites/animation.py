import pyray as pr


class Animation:
    def __init__(
        self,
        frame_start: pr.Vector2,
        frame_size: pr.Vector2,
        frame_count: int,
        frame_per_second: float,
    ) -> None:
        self.frame_start = frame_start
        self.frame_count = frame_count
        self.frame_size = frame_size
        self.frame_per_second = frame_per_second
        self.frame = 0.0

    def get_source(self) -> pr.Rectangle:
        return pr.Rectangle(
            (self.frame_start.x + int(self.frame)) * self.frame_size.x,
            self.frame_start.y * self.frame_size.y,
            self.frame_size.x,
            self.frame_size.y,
        )

    def get_dest(self, x: float, y: float) -> pr.Rectangle:
        return pr.Rectangle(x, y, self.frame_size.x, self.frame_size.y)

    def get_origin(self) -> pr.Vector2:
        return pr.vector2_zero()

    def update(self, dt: float) -> None:
        self.frame += self.frame_per_second * dt
        if int(self.frame) >= self.frame_count:
            self.frame -= int(self.frame)

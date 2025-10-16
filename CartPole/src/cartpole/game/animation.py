import pyray as pr


class Animation:
    def __init__(
        self,
        frame_start: pr.Vector2,
        frame_size: pr.Vector2,
        frame_count: int,
        frame_per_second: float,
        mirror_x: bool = False,
        mirror_y: bool = False,
    ) -> None:
        self.frame_start = frame_start
        self.frame_size = frame_size
        self.frame_count = frame_count
        self.frame_per_second = frame_per_second
        self.mirror_x = -1 if mirror_x else 1
        self.mirror_y = -1 if mirror_y else 1
        self.frame = 0.0

    def get_source(self) -> pr.Rectangle:
        return pr.Rectangle(
            (self.frame_start.x + int(self.frame)) * self.frame_size.x,
            self.frame_start.y * self.frame_size.y,
            self.frame_size.x * self.mirror_x,
            self.frame_size.y * self.mirror_y,
        )

    def update(self, dt: float) -> None:
        self.frame += self.frame_per_second * dt
        if int(self.frame) >= self.frame_count:
            self.frame -= int(self.frame)

from enum import IntFlag

import pyray as pr


class AnimationFlag(IntFlag):
    NONE = 0
    MIRROR_X = 1
    MIRROR_Y = 2


class Animation:
    def __init__(
        self,
        frame_start: pr.Vector2,
        frame_size: pr.Vector2,
        frame_count: int,
        frame_per_second: float,
        flags=AnimationFlag.NONE,
    ) -> None:
        self.frame_start = frame_start
        self.frame_count = frame_count
        self.frame_size = frame_size
        self.frame_per_second = frame_per_second
        self.frame = 0.0

        self.source = pr.Rectangle(
            self.frame_start.x * self.frame_size.x,
            self.frame_start.y * self.frame_size.y,
            self.frame_size.x * (-1 if AnimationFlag.MIRROR_X in flags else 1),
            self.frame_size.y * (-1 if AnimationFlag.MIRROR_Y in flags else 1),
        )
        self.dest = pr.Rectangle(0, 0, self.frame_size.x, self.frame_size.y)
        self.origin = pr.vector2_zero()

    def get_source(self) -> pr.Rectangle:
        self.source.x = (self.frame_start.x + int(self.frame)) * self.frame_size.x
        return self.source

    def get_dest(self, x: float, y: float) -> pr.Rectangle:
        self.dest.x = x
        self.dest.y = y
        return self.dest

    def get_origin(self) -> pr.Vector2:
        return self.origin

    def update(self, dt: float) -> None:
        self.frame += self.frame_per_second * dt
        if int(self.frame) >= self.frame_count:
            self.frame -= int(self.frame)

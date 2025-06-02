from contextlib import contextmanager

import pyray as pr


class DrawCommand:
    def __init__(self, layer: int, depth: float):
        self.layer = layer
        self.depth = depth

    def __call__(self):
        pass

    def __lt__(self, other):
        return self._cmp_depth(other) < 0

    #
    # Private helpers
    #

    def _cmp_depth(self, other) -> float:
        return (self.depth - other.depth) if other.layer == self.layer else (self.layer - other.layer)


class DrawHeap:
    queue: list[DrawCommand] = []


@contextmanager
def begin_draw(camera: pr.Camera2D):
    pr.begin_mode_2d(camera)

    yield None

    for draw in sorted(DrawHeap.queue):
        draw()
    DrawHeap.queue.clear()
    pr.end_mode_2d()


def emit_draw_command(command: DrawCommand):
    DrawHeap.queue.append(command)

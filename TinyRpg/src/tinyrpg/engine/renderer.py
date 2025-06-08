from contextlib import contextmanager
from typing import Callable, Optional, Protocol

import pyray as pr


class RendererSortedDraw(Protocol):
    def get_layer(self) -> int: ...

    def get_depth(self) -> float: ...


class RendererDraw:
    def __init__(self, layer: int, depth: float, draw_func: Optional[Callable[[], None]] = None):
        self.layer = layer
        self.depth = depth
        self.draw_func = draw_func

    def __call__(self):
        if self.draw_func:
            self.draw_func()

    def __lt__(self, other):
        return self._cmp_depth(other) < 0

    #
    # Private helpers
    #

    def _cmp_depth(self, other) -> float:
        return (self.depth - other.depth) if other.layer == self.layer else (self.layer - other.layer)


class RendererHeap:
    queue: list[RendererDraw] = []


@contextmanager
def begin_renderer_draw(camera: pr.Camera2D):
    pr.begin_mode_2d(camera)

    yield None

    for draw in sorted(RendererHeap.queue):
        draw()
    RendererHeap.queue.clear()
    pr.end_mode_2d()


def renderer_sorted_draw(draw_func):
    def wrapper(self: RendererSortedDraw):
        def draw_func_with_self(self=self):
            draw_func(self)

        RendererHeap.queue.append(RendererDraw(self.get_layer(), self.get_depth(), draw_func_with_self))

    return wrapper


def renderer_unsorted_draw(draw_func):
    def wrapper(self):
        def draw_func_with_self(self=self):
            draw_func(self)

        RendererHeap.queue.append(RendererDraw(99, 0, draw_func_with_self))

    return wrapper

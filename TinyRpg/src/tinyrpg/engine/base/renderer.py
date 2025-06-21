from contextlib import contextmanager
from typing import Any, Callable, Protocol

import pyray as pr

from tinyrpg.constants import DEBUG_ENABLED, WORLD_DEBUG_LAYER, WORLD_FOREGROUND_LAYER, WORLD_LAYER_COUNT


class Renderer(Protocol):
    def get_layer(self) -> int: ...

    def get_depth(self) -> float: ...

    def draw(self): ...


class RendererCaller:
    def __init__(self, renderer: Renderer, draw_method: Callable[[Any], None]):
        self.renderer = renderer
        self.draw_method = draw_method
        self.depth = renderer.get_depth()

    def __lt__(self, other):
        return self.depth < other.depth

    def draw(self):
        self.draw_method(self.renderer)


class RendererHeap:
    layers: list[list[RendererCaller]] = [[] for _ in range(WORLD_LAYER_COUNT)]
    sorted_mask: list[bool] = [i == WORLD_FOREGROUND_LAYER for i in range(WORLD_LAYER_COUNT)]


class BoundingBoxRenderer:
    def __init__(self, bbox: pr.BoundingBox):
        self.bbox = bbox

    def get_layer(self) -> int:
        return WORLD_DEBUG_LAYER

    def get_depth(self) -> float:
        return 0

    def draw(self):
        if not DEBUG_ENABLED:
            return

        def draw_method(self):
            pr.draw_bounding_box(self.bbox, pr.GREEN)

        RendererHeap.layers[self.get_layer()].append(RendererCaller(self, draw_method))


class LineRenderer:
    def __init__(self, p1: pr.Vector2, p2: pr.Vector2):
        self.p1 = p1
        self.p2 = p2

    def get_layer(self) -> int:
        return WORLD_DEBUG_LAYER

    def get_depth(self) -> float:
        return 0

    def draw(self):
        if not DEBUG_ENABLED:
            return

        def draw_method(self):
            pr.draw_line_v(self.p1, self.p2, pr.GREEN)

        RendererHeap.layers[self.get_layer()].append(RendererCaller(self, draw_method))


@contextmanager
def begin_mode_sorted_2d(camera: pr.Camera2D):
    pr.begin_mode_2d(camera)

    yield None

    for i in range(WORLD_LAYER_COUNT):
        callers = sorted(RendererHeap.layers[i]) if RendererHeap.sorted_mask[i] else RendererHeap.layers[i]
        for caller in callers:
            caller.draw()

    pr.end_mode_2d()

    for i in range(WORLD_LAYER_COUNT):
        RendererHeap.layers[i].clear()


def renderer(draw_method: Callable[[Any], None]) -> Callable[[Renderer], None]:
    def wrapper(self: Renderer):
        RendererHeap.layers[self.get_layer()].append(RendererCaller(self, draw_method))

    return wrapper

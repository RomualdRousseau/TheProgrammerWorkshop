from contextlib import contextmanager
from typing import Any, Callable, Protocol

import pyray as pr


class Renderer(Protocol):
    def draw(self): ...


class RendererCaller:
    def __init__(self, renderer: Renderer, draw_method: Callable[[Any], None]):
        self.renderer = renderer
        self.draw_method = draw_method

    def draw(self):
        self.draw_method(self.renderer)


class RendererSorted(Renderer):
    def get_layer(self) -> int: ...

    def get_depth(self) -> float: ...


class RendererSortedCaller(RendererCaller):
    def __init__(self, renderer: RendererSorted, draw_method: Callable[[Any], None]):
        super().__init__(renderer, draw_method)
        self.depth = renderer.get_depth()

    def __lt__(self, other):
        return self.depth < other.depth


class RendererHeap:
    layer_0: list[RendererCaller] = []
    layer_1: list[RendererSortedCaller] = []


@contextmanager
def begin_mode_sorted_2d(camera: pr.Camera2D):
    pr.begin_mode_2d(camera)

    yield None

    for renderer in RendererHeap.layer_0:
        renderer.draw()
    for renderer in sorted(RendererHeap.layer_1):
        renderer.draw()

    pr.end_mode_2d()

    RendererHeap.layer_0.clear()
    RendererHeap.layer_1.clear()


def renderer_sorted(draw_method):
    def wrapper(self):
        match self.get_layer():
            case 0:
                RendererHeap.layer_0.append(RendererCaller(self, draw_method))
            case 1:
                RendererHeap.layer_1.append(RendererSortedCaller(self, draw_method))
            case _:
                raise ValueError("Invalid layer")

    return wrapper

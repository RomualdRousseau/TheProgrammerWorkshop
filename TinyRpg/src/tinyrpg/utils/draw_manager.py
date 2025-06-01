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

    def _cmp_depth(self, other) -> float:
        return (self.depth - other.depth) if other.layer == self.layer else (self.layer - other.layer)


class DrawRectangle(DrawCommand):
    def __init__(self, layer: int, depth_ratio: float, rect: pr.Rectangle, color: pr.Color):
        super().__init__(layer, rect.y + rect.height * depth_ratio)
        self.rect = rect
        self.color = color

    def __call__(self):
        pr.draw_rectangle_rec(self.rect, self.color)


class DrawBoundingBox(DrawCommand):
    def __init__(self, bbox: pr.BoundingBox, color: pr.Color):
        super().__init__(99, 0)
        self.bbox = bbox
        self.color = color

    def __call__(self):
        pr.draw_bounding_box(self.bbox, self.color)


class DrawTextureCommand(DrawCommand):
    def __init__(
        self,
        layer: int,
        depth_ratio: float,
        texture: pr.Texture,
        source: pr.Rectangle,
        dest: pr.Rectangle,
        origin: pr.Vector2,
        rotation: float,
    ):
        super().__init__(layer, dest.y + dest.height * depth_ratio)
        self.texture = texture
        self.source = source
        self.dest = dest
        self.origin = origin
        self.rotation = rotation

    def __call__(self):
        pr.draw_texture_pro(
            self.texture,
            self.source,
            self.dest,
            self.origin,
            self.rotation,
            pr.WHITE,
        )


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

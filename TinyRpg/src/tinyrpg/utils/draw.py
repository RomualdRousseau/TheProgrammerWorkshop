import heapq

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
    def __init__(self, layer: int, ratioz: float, rect: pr.Rectangle, color: pr.Color):
        super().__init__(layer, rect.y + rect.height * ratioz)
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
        ratioz: float,
        texture: pr.Texture,
        source: pr.Rectangle,
        dest: pr.Rectangle,
        origin: pr.Vector2,
        rotation: float,
    ):
        super().__init__(layer, dest.y + dest.height * ratioz)
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


def begin_draw() -> None:
    DrawHeap.queue.clear()


def emit_draw_command(command: DrawCommand) -> None:
    heapq.heappush(DrawHeap.queue, command)


def end_draw() -> None:
    [draw() for draw in sorted(DrawHeap.queue)]

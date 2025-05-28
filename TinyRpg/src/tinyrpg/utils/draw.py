import heapq

import pyray as pr


class DrawCommand:
    def __init__(self, layer: int, depth: float):
        self.layer = layer
        self.depth = depth

    def __call__(self):
        pass

    def __lt__(self, other):
        return self._cmp(other) < 0

    def _cmp(self, other) -> int:
        return int(self.depth - other.depth) if other.layer == self.layer else (self.layer - other.layer)


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


def emit_draw_command(command: DrawTextureCommand) -> None:
    heapq.heappush(DrawHeap.queue, command)


def end_draw() -> None:
    while DrawHeap.queue:
        heapq.heappop(DrawHeap.queue)()

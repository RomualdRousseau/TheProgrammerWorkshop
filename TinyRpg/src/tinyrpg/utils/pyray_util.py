import heapq

import pyray as pr
from pytmx import TiledMap


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


class CachedImages:
    textures: dict[str, pr.Texture] = {}


def load_tiledmap(filename: str) -> TiledMap:
    def _pyray_loader(filename, colorkey, **kwargs):
        texture = CachedImages.textures.get(filename)
        if not texture:
            texture = pr.load_texture(filename)
            CachedImages.textures[filename] = texture

        def extract_image(rect, flags):
            x, y, width, height = rect
            return (texture, pr.Rectangle(x, y, width, height), flags)

        return extract_image

    return TiledMap(filename, image_loader=_pyray_loader)


def unload_tiledmap(tiledmap: TiledMap) -> None:
    for texture in CachedImages.textures.values():
        pr.unload_texture(texture)


def draw_tiledmap(tiledmap: TiledMap, pos: pr.Vector2, size: pr.Vector2) -> None:
    origin = pr.vector2_zero()
    for i_layer, layer in enumerate(tiledmap.layers):
        for x, y, (texture, source, _) in layer.tiles():
            dest = pr.Rectangle((pos.x + x) * size.x, (pos.y + y) * size.y, size.x, size.y)
            emit_draw_command(DrawTextureCommand(i_layer, 1.0, texture, source, dest, origin, 0.0))


def begin_draw_queue() -> None:
    DrawHeap.queue = []


def emit_draw_command(command: DrawTextureCommand) -> None:
    heapq.heappush(DrawHeap.queue, command)


def end_draw_queue() -> None:
    while DrawHeap.queue:
        heapq.heappop(DrawHeap.queue)()

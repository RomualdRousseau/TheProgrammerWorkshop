import heapq

import pyray as pr
from pytmx import TiledMap


class SpriteCommand:
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
        self.layer = layer
        self.pos_y = dest.y + dest.height * ratioz
        self.call = lambda: pr.draw_texture_pro(
            texture,
            source,
            dest,
            origin,
            rotation,
            pr.WHITE,
        )

    def _cmp(self, other) -> int:
        return int(self.pos_y - other.pos_y) if other.layer == self.layer else (self.layer - other.layer)

    def __lt__(self, other):
        return self._cmp(other) < 0


class SpriteHeap:
    queue: list[SpriteCommand] = []


class CachedImages:
    textures: dict[str, pr.Texture] = {}


def load_tiledmap(filename: str) -> TiledMap:
    return TiledMap(filename, image_loader=_pyray_loader)


def unload_tiledmap(tiledmap: TiledMap) -> None:
    for texture in CachedImages.textures.values():
        pr.unload_texture(texture)


def draw_tiledmap(tiledmap: TiledMap, pos: pr.Vector2, size: pr.Vector2) -> None:
    origin = pr.vector2_zero()
    for i_layer, layer in enumerate(tiledmap.layers):
        for x, y, (texture, source, _) in layer.tiles():
            dest = pr.Rectangle((pos.x + x) * size.x, (pos.y + y) * size.y, size.x, size.y)
            put_sprite_queue(SpriteCommand(i_layer, 1.0, texture, source, dest, origin, 0.0))


def begin_sprite_queue() -> None:
    SpriteHeap.queue = []


def put_sprite_queue(command: SpriteCommand) -> None:
    heapq.heappush(SpriteHeap.queue, command)


def end_sprite_queue() -> None:
    while SpriteHeap.queue:
        heapq.heappop(SpriteHeap.queue).call()


def _pyray_loader(filename, colorkey, **kwargs):
    texture = CachedImages.textures.get(filename)
    if not texture:
        texture = pr.load_texture(filename)
        CachedImages.textures[filename] = texture

    def extract_image(rect, flags):
        x, y, width, height = rect
        return (texture, pr.Rectangle(x, y, width, height), flags)

    return extract_image

from dataclasses import dataclass

import pyray as pr
from pytmx import TiledMap

from tinyrpg.resources import RESOURCES, load_tile_texture
from tinyrpg.utils.draw import DrawTextureCommand, emit_draw_command


@dataclass
class CachedTile:
    texture: pr.Texture
    source: pr.Rectangle
    ratioz: float


def load_tiledmap(name: str) -> TiledMap:
    def image_loader(filename, colorkey, **kwargs):
        tile_texture = load_tile_texture(filename)

        def extract_image(rect, flags):
            return CachedTile(tile_texture, pr.Rectangle(*rect), 1.0)

        return extract_image

    tiledmap = TiledMap(RESOURCES[name], image_loader=image_loader)
    for layer_i, layer in enumerate(tiledmap.layers):
        for x, y, tile in layer.tiles():
            prop = tiledmap.get_tile_properties(x, y, layer_i)
            if prop:
                tile.ratioz = prop.get("depth", 1.0)

    return tiledmap


def draw_tiledmap(tiledmap: TiledMap, pos: pr.Vector2) -> None:
    origin = pr.vector2_zero()
    for layer_i, layer in enumerate(tiledmap.layers):
        for x, y, tile in layer.tiles():
            size_x, size_y = tile.source.width, tile.source.height
            dest = pr.Rectangle((pos.x + x) * size_x, (pos.y + y) * size_y, size_x, size_y)
            emit_draw_command(DrawTextureCommand(layer_i, tile.ratioz, tile.texture, tile.source, dest, origin, 0.0))

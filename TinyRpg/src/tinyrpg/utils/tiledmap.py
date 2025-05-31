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
    walkable: bool


@dataclass
class CachedTiledMap:
    map: TiledMap
    bboxes: list[tuple[float, float, CachedTile]]


def get_bbox(x: float, y: float, tile: CachedTile, pos: pr.Vector2) -> pr.BoundingBox:
    size_x, size_y = tile.source.width, tile.source.height
    min = pr.Vector3((x + pos.x) * size_x + 2, (y + pos.y) * size_y + 2, 0)
    max = pr.Vector3(min.x + size_x - 1 - 4, min.y + size_y - 1 - 4, 0)
    return pr.BoundingBox(min, max)


def get_dest(x: float, y: float, tile: CachedTile, pos: pr.Vector2) -> pr.Rectangle:
    size_x, size_y = tile.source.width, tile.source.height
    return pr.Rectangle((x + pos.x) * size_x, (y + pos.y) * size_y, size_x, size_y)


def load_tiledmap(name: str) -> CachedTiledMap:
    def image_loader(filename, colorkey, **kwargs):
        tile_texture = load_tile_texture(filename)

        def extract_image(rect, flags):
            return CachedTile(tile_texture, pr.Rectangle(*rect), 1.0, True)

        return extract_image

    tiledmap = CachedTiledMap(TiledMap(RESOURCES[name], image_loader=image_loader), [])

    for layer_i, layer in enumerate(tiledmap.map.layers):
        for x, y, tile in layer.tiles():
            prop = tiledmap.map.get_tile_properties(x, y, layer_i)
            if prop:
                tile.ratioz = prop.get("depth", 1.0)
                tile.walkable = prop.get("walkable", True)
                if not tile.walkable:
                    tiledmap.bboxes.append((x, y, tile))

    return tiledmap


def collide_tiledmap_bbox(
    tiledmap: CachedTiledMap, pos: pr.Vector2, bbox1: pr.BoundingBox, collision_vector: pr.Vector2
) -> pr.Vector2:
    sum = pr.vector3_zero()
    for bbox2 in (get_bbox(*x, pos) for x in tiledmap.bboxes):
        if pr.check_collision_boxes(bbox1, bbox2):
            mid1 = pr.vector3_scale(pr.vector3_add(bbox1.min, bbox1.max), 0.5)
            mid2 = pr.vector3_scale(pr.vector3_add(bbox2.min, bbox2.max), 0.5)
            sum = pr.vector3_add(sum, pr.vector3_subtract(mid1, mid2))
    return pr.vector2_add(collision_vector, pr.vector2_normalize(pr.Vector2(sum.x, sum.y)))


def draw_tiledmap(tiledmap: CachedTiledMap, pos: pr.Vector2) -> None:
    origin = pr.vector2_zero()
    for layer_i, layer in enumerate(tiledmap.map.layers):
        for x, y, tile in layer.tiles():
            emit_draw_command(
                DrawTextureCommand(
                    layer_i, tile.ratioz, tile.texture, tile.source, get_dest(x, y, tile, pos), origin, 0.0
                )
            )

    # for x, y, tile in tiledmap.bboxes:
    #     emit_draw_command(DrawBoundingBox(get_bbox(x, y, tile, pos), pr.color_alpha(pr.RED, 0.5)))

from dataclasses import dataclass

import pyray as pr
from pytmx import TiledMap

from tinyrpg.engine.draw_command import DrawTextureCommand
from tinyrpg.engine.draw_manager import emit_draw_command
from tinyrpg.utils.bbox import get_bbox_center, get_bbox_from_rect
from tinyrpg.utils.quad_tree import QuadTreeBuilder

MAP_BBOX = pr.BoundingBox((2, 2, 0), (-2, -2, 0))


@dataclass
class MapTile:
    texture: pr.Texture
    source: pr.Rectangle
    depth_ratio: float = 1.0
    walkable: bool = False


MapBoundingBox = tuple[pr.BoundingBox, MapTile]


class Map:
    def __init__(self, tiledmap: TiledMap):
        self.tiledmap = tiledmap
        self.origin = pr.Vector2(-tiledmap.width // 2, -tiledmap.height // 2)
        self.bboxes = QuadTreeBuilder[MapBoundingBox](tiledmap.width, tiledmap.tilewidth).build()

        if self.tiledmap.background_color:
            r, g, b = [int(self.tiledmap.background_color[i : i + 2], 16) for i in (1, 3, 5)]
            self.background_color = pr.Color(r, g, b, 255)
        else:
            self.background_color = pr.RAYWHITE

        for layer_i, layer in enumerate(tiledmap.layers):
            for x, y, tile in layer.tiles():
                prop = tiledmap.get_tile_properties(x, y, layer_i)
                if not prop:
                    continue

                tile.depth_ratio = prop.get("depth_ratio", prop.get("depth", 1.0))

                tile.walkable = prop.get("walkable", True)
                if not tile.walkable:
                    self.bboxes.append(self.get_tilemap_to_world(x, y), (self.get_bbox(x, y), tile))

    def get_background_color(self):
        return self.background_color

    def get_bbox(self, x: float, y: float) -> pr.BoundingBox:
        return get_bbox_from_rect(self._get_dest(x, y))

    def get_tilemap_to_world(self, x: float, y: float) -> pr.Vector2:
        size_x, size_y = self.tiledmap.tilewidth, self.tiledmap.tileheight
        return pr.Vector2((x + self.origin.x) * size_x, (y + self.origin.y) * size_y)

    def check_collide_bbox(self, bbox: pr.BoundingBox, collision_vector: pr.Vector2) -> tuple[bool, pr.Vector2]:
        has_collision = False
        sum_reaction = pr.vector3_zero()
        for bbox2, _ in self.bboxes.find_bbox(bbox):
            if pr.check_collision_boxes(bbox, bbox2):
                v = pr.vector3_subtract(get_bbox_center(bbox), get_bbox_center(bbox2))
                if abs(v.x) >= abs(v.y):
                    sum_reaction.x = max(min(sum_reaction.x + v.x / abs(v.x), 1), -1)
                if abs(v.y) >= abs(v.x):
                    sum_reaction.y = max(min(sum_reaction.y + v.y / abs(v.y), 1), -1)
                has_collision |= True
        sum_reaction_2d = pr.vector2_normalize(pr.Vector2(sum_reaction.x, sum_reaction.y))
        return has_collision, pr.vector2_add(collision_vector, sum_reaction_2d)

    def draw(self) -> None:
        origin = pr.vector2_zero()
        for layer_i, layer in enumerate(self.tiledmap.layers):
            for x, y, tile in layer.tiles():
                emit_draw_command(
                    DrawTextureCommand(
                        layer_i, tile.depth_ratio, tile.texture, tile.source, self._get_dest(x, y), origin, 0.0
                    )
                )

    #
    # Private helpers
    #

    def _get_dest(self, x: float, y: float) -> pr.Rectangle:
        size_x, size_y = self.tiledmap.tilewidth, self.tiledmap.tileheight
        return pr.Rectangle((x + self.origin.x) * size_x, (y + self.origin.y) * size_y, size_x, size_y)

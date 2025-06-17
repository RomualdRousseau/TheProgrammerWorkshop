from dataclasses import dataclass
from typing import Optional

import pyray as pr
from pytmx import TiledMap, TiledObjectGroup, TiledTileLayer

from tinyrpg.constants import WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine.renderer import renderer
from tinyrpg.utils.bbox import (
    check_collision_bbox_ray,
    expand_bbox,
    get_bbox_center,
    get_bbox_center_2d,
    get_bbox_from_rect,
)
from tinyrpg.utils.quad_tree import QuadTreeBuilder


@dataclass
class MapTile:
    texture: pr.Texture
    source: pr.Rectangle
    depth_ratio: float = 1.0
    walkable: bool = False


class MapTileRenderer:
    def __init__(self, tile: MapTile, dest: pr.Rectangle, layer: int):
        self.tile = tile
        self.dest = dest
        self.layer = layer
        self.depth = self.dest.y + self.dest.height * self.tile.depth_ratio

    def get_layer(self) -> int:
        return self.layer

    def get_depth(self) -> float:
        return self.depth

    @renderer
    def draw(self):
        pr.draw_texture_pro(
            self.tile.texture,
            self.tile.source,
            self.dest,
            pr.vector2_zero(),
            0.0,
            pr.WHITE,
        )


class MapTrigger:
    def __init__(self, pos: pr.Vector2, size: float):
        self.pos = pos
        self.size = size
        self.trigerred = False


class MapObject:
    def __init__(self, pos: pr.Vector2, type: str, name: str):
        self.pos = pos
        self.type = type
        self.name = name


MapBoundingBox = tuple[pr.BoundingBox, MapTile]


class Map:
    def __init__(self, tiledmap: TiledMap):
        self.tiledmap = tiledmap
        self.origin = pr.Vector2(-tiledmap.width // 2, -tiledmap.height // 2)
        self.start_location = pr.vector2_zero()
        self.bboxes = QuadTreeBuilder[MapBoundingBox](tiledmap.width, tiledmap.tilewidth).build()
        self.tiles: list[MapTileRenderer] = []
        self.triggers: list[MapTrigger] = []
        self.objects: list[MapObject] = []

        if self.tiledmap.background_color:
            r, g, b = [int(self.tiledmap.background_color[i : i + 2], 16) for i in (1, 3, 5)]
            self.background_color = pr.Color(r, g, b, 255)
        else:
            self.background_color = pr.RAYWHITE

        for layer in tiledmap.layers:
            match layer:
                case TiledTileLayer():
                    for x, y, tile in layer.tiles():
                        prop = tiledmap.get_tile_properties(x, y, layer.id - 1)
                        if not prop:
                            continue

                        tile.depth_ratio = prop.get("depth_ratio", prop.get("depth", 1.0))

                        tile.walkable = prop.get("walkable", True)
                        if not tile.walkable:
                            self.bboxes.append(self._get_tilexy_to_world_2d(x, y), (self.get_tile_bbox(x, y), tile))

                        self.tiles.append(MapTileRenderer(tile, self._get_tilexy_dest(x, y), layer.id - 1))
                case TiledObjectGroup():
                    for object in layer:
                        match object.properties["type"]:
                            case "start":
                                self.start_location = self._get_xy_to_world_2d(object.x, object.y)
                            case "trigger":
                                size = object.properties["size"]
                                self.triggers.append(MapTrigger(self._get_xy_to_world_2d(object.x, object.y), size))
                            case "enemy" | "npc" as type:
                                name = object.properties["name"]
                                self.objects.append(MapObject(self._get_xy_to_world_2d(object.x, object.y), type, name))

    def get_world_boundary(self) -> pr.BoundingBox:
        x = (self.tiledmap.width * self.tiledmap.tilewidth - WORLD_WIDTH) // 2
        y = (self.tiledmap.height * self.tiledmap.tileheight - WORLD_HEIGHT) // 2
        return pr.BoundingBox((-x, -y, -1), (x, y, 1))

    def get_tile_bbox(self, x: float, y: float) -> pr.BoundingBox:
        return get_bbox_from_rect(self._get_tilexy_dest(x, y))

    def check_los(self, p1: pr.Vector2, p2: pr.Vector2) -> bool:
        dir = pr.vector2_subtract(p2, p1)
        dist1 = pr.vector2_length(dir)
        ray = pr.Ray(pr.Vector3(p1.x, p1.y), pr.vector3_normalize(pr.Vector3(dir.x, dir.y)))
        has_obstacle = False
        for bbox, _ in self.bboxes.find_ray(ray):
            if check_collision_bbox_ray(bbox, ray):
                dist2 = pr.vector2_distance(p1, get_bbox_center_2d(bbox))
                has_obstacle |= dist1 > dist2
        return not has_obstacle

    def check_collision(
        self, bbox: pr.BoundingBox, collision_vector: Optional[pr.Vector2] = None
    ) -> tuple[bool, pr.Vector2]:
        has_collision = False
        sum_reaction = pr.vector3_zero()
        bbox1 = expand_bbox(bbox, pr.Vector2(self.tiledmap.tilewidth * 0.5, self.tiledmap.tileheight * 0.5))
        # BoundingBoxRenderer(bbox).draw()
        # BoundingBoxRenderer(bbox1).draw()
        for bbox2, _ in self.bboxes.find_bbox(bbox1):
            # BoundingBoxRenderer(bbox2).draw()
            if pr.check_collision_boxes(bbox, bbox2):
                sum_reaction = pr.vector3_add(
                    sum_reaction, pr.vector3_subtract(get_bbox_center(bbox), get_bbox_center(bbox2))
                )
                has_collision |= True
        sum_reaction_2d = pr.vector2_normalize(pr.Vector2(sum_reaction.x, sum_reaction.y))
        return has_collision, pr.vector2_add(collision_vector or pr.vector2_zero(), sum_reaction_2d)

    def check_triggers(self, pos: pr.Vector2) -> bool:
        has_collision = False
        for trigger in self.triggers:
            has_collision |= pr.vector2_distance(pos, trigger.pos) <= trigger.size
            if has_collision and not trigger.trigerred:
                trigger.trigerred = True
                return True
            if not has_collision and trigger.trigerred:
                trigger.trigerred = False
        return False

    def draw(self) -> None:
        for tile in self.tiles:
            tile.draw()

    #
    # Private helpers
    #

    def _get_xy_to_world_2d(self, x: float, y: float) -> pr.Vector2:
        size_x, size_y = self.tiledmap.tilewidth, self.tiledmap.tileheight
        return pr.Vector2(x + self.origin.x * size_x, y + self.origin.y * size_y)

    def _get_tilexy_to_world_2d(self, x: float, y: float) -> pr.Vector2:
        size_x, size_y = self.tiledmap.tilewidth, self.tiledmap.tileheight
        return pr.Vector2((x + self.origin.x + 0.5) * size_x, (y + self.origin.y + 0.5) * size_y)

    def _get_tilexy_dest(self, x: float, y: float) -> pr.Rectangle:
        size_x, size_y = self.tiledmap.tilewidth, self.tiledmap.tileheight
        return pr.Rectangle((x + self.origin.x) * size_x, (y + self.origin.y) * size_y, size_x, size_y)

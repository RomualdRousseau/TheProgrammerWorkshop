from __future__ import annotations

import math
from functools import partial, reduce
from typing import Callable, Generator, Generic, Optional, TypeVar

import pyray as pr

from tinyrpg.utils.bbox import check_collision_bbox_point, check_collision_bbox_ray, subdivide_bbox

T = TypeVar("T")


class QuadTreeBuilder(Generic[T]):
    def __init__(self, size: float, spacing: float):
        self.size = size
        self.spacing = spacing

    def build(self) -> QuadTree[T]:
        bound = self.size * self.spacing / 2
        bbox = pr.BoundingBox((-bound, -bound, -1), (bound, bound, 1))
        depth = int(math.log2(self.size))
        return QuadTree[T](bbox).build_tree(depth)


class QuadTree(Generic[T]):
    def __init__(self, bbox: pr.BoundingBox, parent: Optional[QuadTree[T]] = None):
        self.parent = parent
        self.bbox = bbox
        self.entities: list[T] = []
        self.children: list[QuadTree[T]] = []

    def build_tree(self, depth: int) -> QuadTree[T]:
        if depth > 1:
            self.children = [QuadTree[T](bbox, self).build_tree(depth - 1) for bbox in subdivide_bbox(self.bbox)]
        return self

    def walk_tree(self, check_collide: Callable[[pr.BoundingBox], bool]) -> Generator[QuadTree[T]]:
        if check_collide(self.bbox):
            match self.children:
                case []:
                    yield self
                case _:
                    for child in self.children:
                        yield from child.walk_tree(check_collide)

    def find_point(self, point: pr.Vector2) -> list[T]:
        node = next(self.walk_tree(partial(check_collision_bbox_point, point=point)), None)
        return node.entities if node else []

    def find_ray(self, ray: pr.Ray) -> list[T]:
        nodes = self.walk_tree(partial(check_collision_bbox_ray, ray=ray))
        return reduce(lambda x, y: x + y.entities, nodes, [])

    def find_bbox(self, bbox: pr.BoundingBox) -> list[T]:
        nodes = self.walk_tree(partial(pr.check_collision_boxes, bbox))
        return reduce(lambda x, y: x + y.entities, nodes, [])

    def append(self, point: pr.Vector2, entity: T) -> Optional[QuadTree[T]]:
        node = next(self.walk_tree(partial(check_collision_bbox_point, point=point)), None)
        if node:
            node.entities.append(entity)
        return node

    def remove(self, point: pr.Vector2, entity: T) -> Optional[QuadTree[T]]:
        node = next(self.walk_tree(partial(check_collision_bbox_point, point=point)), None)
        if node:
            node.entities.remove(entity)
        return node

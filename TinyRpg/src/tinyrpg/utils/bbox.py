from typing import Iterable

import pyray as pr


def get_bbox_center(bbox: pr.BoundingBox) -> pr.Vector3:
    return pr.vector3_scale(pr.vector3_add(bbox.min, bbox.max), 0.5)


def subdivide_bbox(bbox: pr.BoundingBox) -> Iterable[pr.BoundingBox]:
    a, b, m = bbox.min, bbox.max, get_bbox_center(bbox)
    yield pr.BoundingBox(pr.Vector3(a.x, a.y, 0), pr.Vector3(m.x, m.y, 0))
    yield pr.BoundingBox(pr.Vector3(m.x, a.y, 0), pr.Vector3(b.x, m.y, 0))
    yield pr.BoundingBox(pr.Vector3(m.x, m.y, 0), pr.Vector3(b.x, b.y, 0))
    yield pr.BoundingBox(pr.Vector3(a.x, m.y, 0), pr.Vector3(m.x, b.y, 0))


def check_collision_bbox_point(bbox: pr.BoundingBox, point: pr.Vector2) -> bool:
    return bbox.min.x <= point.x < bbox.max.x and bbox.min.y <= point.y < bbox.max.y

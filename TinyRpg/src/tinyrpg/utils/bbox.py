from typing import Iterable

import pyray as pr


def get_bbox_from_rect(rect: pr.Rectangle) -> pr.BoundingBox:
    min = pr.Vector3(rect.x, rect.y, 0)
    max = pr.Vector3(rect.x + rect.width - 1, rect.y + rect.height - 1, 0)
    return pr.BoundingBox(min, max)


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


def check_collision_bbox_ray(bbox: pr.BoundingBox, ray: pr.Ray) -> bool:
    col = pr.get_ray_collision_box(ray, bbox)
    return col.hit

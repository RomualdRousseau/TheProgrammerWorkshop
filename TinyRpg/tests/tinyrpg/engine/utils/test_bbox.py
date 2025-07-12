import pyray as pr
import pytest

import tinyrpg.engine.utils.bbox as bbox


@pytest.fixture
def setup_data():
    rect = pr.Rectangle(0, 0, 10, 10)
    bbox_ = bbox.get_bbox_from_rect(rect)
    center = pr.Vector3(4.5, 4.5, 0)
    point_inside = pr.Vector2(2, 2)
    point_outside = pr.Vector2(11, 11)
    ray_inside = pr.Ray(pr.Vector3(2, 2, 0), pr.Vector3(1, 0, 0))
    ray_outside = pr.Ray(pr.Vector3(11, 11, 0), pr.Vector3(1, 0, 0))
    return {
        "rect": rect,
        "bbox": bbox_,
        "center": center,
        "point_inside": point_inside,
        "point_outside": point_outside,
        "ray_inside": ray_inside,
        "ray_outside": ray_outside,
    }


def test_get_bbox_from_rect(setup_data):
    assert pr.vector3_equals(setup_data["bbox"].min, pr.Vector3(0, 0, -1))
    assert pr.vector3_equals(setup_data["bbox"].max, pr.Vector3(9, 9, 1))


def test_get_bbox_center(setup_data):
    center = bbox.get_bbox_center(setup_data["bbox"])
    assert pr.vector3_equals(center, setup_data["center"])


def test_get_bbox_center_2d(setup_data):
    assert pr.vector2_equals(bbox.get_bbox_center_2d(setup_data["bbox"]), pr.Vector2(4.5, 4.5))


def test_subdivide_bbox(setup_data):
    subdivisions = list(bbox.subdivide_bbox(setup_data["bbox"]))
    assert len(subdivisions) == 4


def test_resize_bbox(setup_data):
    resized_bbox = bbox.resize_bbox(setup_data["bbox"], pr.Vector2(1, 1))
    assert pr.vector3_equals(resized_bbox.min, pr.Vector3(-1, -1, -1))
    assert pr.vector3_equals(resized_bbox.max, pr.Vector3(10, 10, 1))


def test_adjust_bbox(setup_data):
    adjust = pr.BoundingBox((1, 1, 0), (2, 2, 0))
    adjusted_bbox = bbox.adjust_bbox(setup_data["bbox"], adjust)
    assert pr.vector3_equals(adjusted_bbox.min, pr.Vector3(1, 1, -1))
    assert pr.vector3_equals(adjusted_bbox.max, pr.Vector3(11, 11, 1))


def test_check_collision_bbox_point(setup_data):
    assert bbox.check_collision_bbox_point(setup_data["bbox"], setup_data["point_inside"])
    assert not bbox.check_collision_bbox_point(setup_data["bbox"], setup_data["point_outside"])


def test_check_collision_bbox_ray(setup_data):
    assert bbox.check_collision_bbox_ray(setup_data["bbox"], setup_data["ray_inside"])
    assert not bbox.check_collision_bbox_ray(setup_data["bbox"], setup_data["ray_outside"])

from __future__ import annotations

from functools import partial

import pyray as pr
import pytest

from tinyrpg.engine.utils.bbox import check_collision_bbox_point
from tinyrpg.engine.utils.quad_tree import QuadTreeBuilder


@pytest.fixture
def quad_tree():
    builder = QuadTreeBuilder[float](size=16, spacing=1.0)
    return builder.build()


def test_build_tree(quad_tree):
    assert len(quad_tree.children) == 4
    for child in quad_tree.children:
        assert len(child.children) == 4


def test_walk_tree(quad_tree):
    point = pr.Vector2(0.5, 0.5)
    nodes = list(quad_tree.walk_tree(partial(check_collision_bbox_point, point=point)))
    assert len(nodes) == 1
    assert pr.vector3_equals(nodes[0].bbox.min, (0.0, 0.0, -1))
    assert pr.vector3_equals(nodes[0].bbox.max, (2.0, 2.0, 1))


def test_find_point(quad_tree):
    point = pr.Vector2(0.5, 0.5)
    quad_tree.append(point, 1.0)
    entities = quad_tree.find_point(point)
    assert entities == [1.0]


def test_find_ray(quad_tree):
    ray = pr.Ray((0, 0, 0), (1, 1, 0))
    point = pr.Vector2(0.5, 0.5)
    quad_tree.append(point, 1.0)
    entities = quad_tree.find_ray(ray)
    assert entities == [1.0]


def test_find_bbox(quad_tree):
    bbox = pr.BoundingBox((0, 0, 0), (1, 1, 0))
    point = pr.Vector2(0.5, 0.5)
    quad_tree.append(point, 1.0)
    entities = quad_tree.find_bbox(bbox)
    assert entities == [1.0]


def test_append(quad_tree):
    point = pr.Vector2(0.5, 0.5)
    node = quad_tree.append(point, 1.0)
    assert node is not None
    assert node.entities == [1.0]


def test_remove(quad_tree):
    point = pr.Vector2(0.5, 0.5)
    quad_tree.append(point, 1.0)
    node = quad_tree.remove(point, 1.0)
    assert node is not None
    assert node.entities == []

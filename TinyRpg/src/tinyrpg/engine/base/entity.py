from __future__ import annotations

import math
from random import uniform
from typing import Optional

import pyray as pr

from tinyrpg.constants import ENTITY_DENSITY_DEFAULT, ENTITY_MASS_DEFAULT, EPSILON, MAX_AVOID_FORCE
from tinyrpg.engine.utils.bbox import get_bbox_center, get_bbox_from_rect

GRAVITY_FORCE = pr.Vector2(0, 150)


class Entity:
    def __init__(self, id: str, pos: pr.Vector2):
        self.id = id
        self.mass = ENTITY_MASS_DEFAULT
        self.force = pr.vector2_zero()
        self.vel = pr.vector2_zero()
        self.pos = pos

    def should_be_free(self) -> bool:
        return False

    def get_bbox(self) -> pr.BoundingBox:
        return get_bbox_from_rect(
            pr.Rectangle(self.pos.x, self.pos.y, self.mass * ENTITY_DENSITY_DEFAULT, self.mass * ENTITY_DENSITY_DEFAULT)
        )

    def move_constant(self, speed: pr.Vector2, dt: float):
        mu = self.mass / (dt + EPSILON)
        friction_force = pr.vector2_add(pr.vector2_scale(speed, mu - 1), pr.vector2_scale(self.vel, -mu))
        self.force = pr.vector2_add(self.force, pr.vector2_add(speed, friction_force))

    def random_force(self, max_force: float, min_angle: float, max_angle: float):
        angle = uniform(min_angle, max_angle)
        some_force = pr.Vector2(max_force * math.cos(angle), -max_force * math.sin(angle))
        self.force = pr.vector2_add(self.force, some_force)

    def clamp_force(self, min_force: float, max_force: float):
        self.force = pr.vector2_clamp_value(self.force, min_force, max_force)

    def gravity(self):
        gravity_force = pr.vector2_scale(GRAVITY_FORCE, self.mass)
        self.force = pr.vector2_add(self.force, gravity_force)

    def seek(self, target: pr.Vector2, max_force: float, slowing_radius: float):
        desired_dir = pr.vector2_subtract(target, self.pos)
        dist = pr.vector2_length(desired_dir)
        if dist < slowing_radius:
            desired_force = max_force * dist / slowing_radius
        else:
            desired_force = max_force
        self.force = pr.vector2_add(self.force, pr.vector2_scale(pr.vector2_normalize(desired_dir), desired_force))

    def collide(self, collision_vector: pr.Vector2, other: Optional[Entity] = None):
        avoidance = pr.vector2_scale(collision_vector, MAX_AVOID_FORCE)
        self.force = pr.vector2_add(self.force, avoidance)

    def constrain_to_boundary(self, boundary: pr.BoundingBox):
        self.pos.x = max(boundary.min.x, min(self.pos.x, boundary.max.x))
        self.pos.y = max(boundary.min.y, min(self.pos.y, boundary.max.y))

    def check_collision(
        self, bbox: pr.BoundingBox, collision_vector: Optional[pr.Vector2] = None
    ) -> tuple[bool, pr.Vector2]:
        has_collision, reaction = False, pr.vector2_zero()
        bbox2 = self.get_bbox()
        if pr.check_collision_boxes(bbox, bbox2):
            reaction = pr.vector3_subtract(get_bbox_center(bbox), get_bbox_center(bbox2))
            has_collision = True
        reaction_2d = pr.vector2_normalize(pr.Vector2(reaction.x, reaction.y))
        return has_collision, pr.vector2_add(collision_vector or pr.vector2_zero(), reaction_2d)

    def update(self, dt: float):
        acc = pr.vector2_scale(self.force, 1.0 / self.mass)
        self.vel = pr.vector2_add(self.vel, pr.vector2_scale(acc, dt))
        self.pos = pr.vector2_add(self.pos, pr.vector2_scale(self.vel, dt))
        self.force = pr.vector2_zero()

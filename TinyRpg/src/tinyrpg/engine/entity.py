import pyray as pr

from tinyrpg.constants import DEFAULT_ENTITY_DENSITY, DEFAULT_ENTITY_MASS, EPSILON
from tinyrpg.utils.bbox import get_bbox_from_rect


class Entity:
    def __init__(self, pos: pr.Vector2):
        self.mass = DEFAULT_ENTITY_MASS
        self.force = pr.vector2_zero()
        self.pos = pos
        self.vel = pr.vector2_zero()

    def get_bbox(self) -> pr.BoundingBox:
        return get_bbox_from_rect(
            pr.Rectangle(self.pos.x, self.pos.y, self.mass * DEFAULT_ENTITY_DENSITY, self.mass * DEFAULT_ENTITY_DENSITY)
        )

    def move_constant(self, speed: pr.Vector2, dt: float):
        mu = self.mass / (dt + EPSILON)
        friction = pr.vector2_add(pr.vector2_scale(speed, mu - 1), pr.vector2_scale(self.vel, -mu))
        self.force = pr.vector2_add(self.force, pr.vector2_add(speed, friction))

    def constrain_to_world(self, boundary: pr.BoundingBox):
        self.pos.x = max(boundary.min.x, min(self.pos.x, boundary.max.x))
        self.pos.y = max(boundary.min.y, min(self.pos.y, boundary.max.y))

    def collide(self, collision_vector: pr.Vector2, dt: float):
        # TODO: Sliding effect on walls
        u = pr.vector2_scale(collision_vector, 0.5)
        v = pr.vector2_add(u, pr.vector2_scale(self.vel, -dt))
        self.pos = pr.vector2_add(self.pos, v)

    def update(self, dt: float):
        acc = pr.vector2_scale(self.force, 1 / self.mass)
        self.vel = pr.vector2_add(self.vel, pr.vector2_scale(acc, dt))
        self.pos = pr.vector2_add(self.pos, pr.vector2_scale(self.vel, dt))
        self.force = pr.vector2_zero()

    def draw(self):
        pass

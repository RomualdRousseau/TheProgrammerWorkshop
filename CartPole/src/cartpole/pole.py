import math

import pyray as pr

from cartpole.config import AIR_DRAG, POLE_K, POLE_LENGTH, POLE_MASS, POLE_RADIUS
from cartpole.physic.forces import friction_force, gravity_force, spring_force
from cartpole.physic.rigid_body import RigidBody


class Pole:
    def __init__(self, pivot: RigidBody) -> None:
        self.body = RigidBody(POLE_MASS, pr.Vector2(pivot.pos.x, pivot.pos.y - POLE_LENGTH))
        self.pivot = pivot

    def update(self, dt: float) -> None:
        self.body.apply_force(gravity_force(self.body))
        self.body.apply_force(friction_force(self.body, AIR_DRAG))
        self.body.apply_force(spring_force(self.body, self.pivot.pos, POLE_LENGTH, POLE_K))
        self.body.update(dt)

    def draw(self) -> None:
        pr.draw_line_v(self.pivot.pos, self.body.pos, pr.BLUE)
        pr.draw_circle_v(self.body.pos, POLE_RADIUS, pr.RAYWHITE)

    def get_angle(self) -> float:
        v = pr.vector2_subtract(self.body.pos, self.pivot.pos)
        return -(math.atan2(v.y, v.x) + math.pi / 2)

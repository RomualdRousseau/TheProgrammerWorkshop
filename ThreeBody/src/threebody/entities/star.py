from __future__ import annotations

import pyray as pr

from threebody.utils.physic import centrifuge_force_on_axis_y, euler_integrate
from threebody.utils.sphere import Sphere

STAR_DISTANCE_SCALE = 1e-7
STAR_RADIUS_SCALE = 2e-18
TRAIL_SIZE = 50

ANGULAR_VELOCITY = 1.99  # rad s-1


class Star:
    def __init__(self, pos: pr.Vector3, mass: float) -> None:
        self.mass = mass
        self.pos = pos
        self.force = pr.vector3_zero()
        self.rho = centrifuge_force_on_axis_y(self, ANGULAR_VELOCITY)
        self.sphere = Sphere(TRAIL_SIZE)

    def update(self, dt: float) -> None:
        self.rho = euler_integrate(self.rho, self.force, dt)
        self.pos = euler_integrate(self.pos, pr.vector3_scale(self.rho, 1.0 / self.mass), dt)
        self.reset_force()

    def draw(self) -> None:
        scaled_pos = pr.vector3_scale(self.pos, STAR_DISTANCE_SCALE)
        scaled_radius = self.mass * STAR_RADIUS_SCALE
        self.sphere.draw(scaled_pos, scaled_radius, pr.RAYWHITE)

    def reset_force(self):
        self.force = pr.vector3_zero()

    def apply_force(self, f: pr.Vector3):
        self.force = pr.vector3_add(self.force, f)

import pyray as pr


class RigidBody:
    def __init__(self, mass: float, pos: pr.Vector2) -> None:
        self.mass = mass
        self.pos = pos
        self.vel = pr.vector2_zero()
        self.force = pr.vector2_zero()

    def apply_force(self, force: pr.Vector2) -> None:
        self.force = pr.vector2_add(self.force, force)

    def update(self, dt: float) -> None:
        acc = pr.vector2_scale(self.force, 1 / self.mass)
        self.vel = pr.vector2_add(self.vel, pr.vector2_scale(acc, dt))
        self.pos = pr.vector2_add(self.pos, pr.vector2_scale(self.vel, dt))
        self.force = pr.vector2_zero()

    def draw(self) -> None:
        pass

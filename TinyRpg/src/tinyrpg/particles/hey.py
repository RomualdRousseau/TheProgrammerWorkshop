import pyray as pr

from tinyrpg.engine.particle import Particle
from tinyrpg.resources import load_texture


class Hey(Particle):
    def __init__(self, pos: pr.Vector2):
        super().__init__(load_texture("bubble"), pos)

    def update(self, dt: float):
        self.pos.y -= 30 * dt
        super().update(dt)

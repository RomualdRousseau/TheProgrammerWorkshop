import pyray as pr

from tinyrpg.engine.base.entity import Entity


class Particle(Entity):
    def __init__(self, pos: pr.Vector2):
        super().__init__("particle", pos)
        self.life = 100

    def should_be_free(self) -> bool:
        return self.life <= 0

    def update(self, dt: float):
        self.life = max(self.life - 1, 0)
        super().update(dt)

    def draw(self):
        pass

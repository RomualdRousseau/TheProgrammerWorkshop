import pyray as pr

from tinyrpg.engine.sprite import Sprite


class Particle(Sprite):
    def __init__(self, texture: pr.Texture, pos: pr.Vector2):
        super().__init__(texture, pos)
        self.life = 100

    def is_alive(self) -> bool:
        return self.life > 0

    def update(self, dt: float):
        self.life = max(self.life - 1, 0)
        super().update(dt)

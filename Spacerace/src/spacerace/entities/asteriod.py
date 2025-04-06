from random import random

import pyray as pr

from spacerace import ASTEROID_MASS, ASTEROID_SPEED, WINDOW_WIDTH


class Asteroid:
    def __init__(self, y: float):
        self.x = WINDOW_WIDTH * random()
        self.y = y
        self.l2r = random() < 0.5
        self.speed = (1 if self.l2r else -1) * (0.5 * ASTEROID_SPEED + random() * 0.5 * ASTEROID_SPEED)

    def reset(self):
        self.x = -ASTEROID_MASS if self.l2r else WINDOW_WIDTH
        self.speed = (1 if self.l2r else -1) * (0.5 + random() * 0.5) * 50

    def get_collision_box(self) -> tuple[float, float, float, float]:
        return (
            self.x,
            self.y,
            ASTEROID_MASS,
            2,
        )

    def update(self, dt: float):
        self.x += self.speed * dt

        if not (-ASTEROID_MASS <= self.x <= WINDOW_WIDTH):
            self.reset()

    def draw(self):
        pr.draw_rectangle(int(self.x), int(self.y), ASTEROID_MASS, 2, pr.RAYWHITE)

    def collide(self):
        self.reset()

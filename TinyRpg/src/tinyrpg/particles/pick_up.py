import math

import pyray as pr

from tinyrpg.constants import DEBUG_ENABLED
from tinyrpg.engine import Character, Item, Particle
from tinyrpg.engine.base.resources import load_texture
from tinyrpg.engine.base.sound import play_sound

PICKUP_FORCE_INITIAL = 5000  # N
PICKUP_FORCE_SEEK = 1100  # N
PICKUP_WIDTH = 16  # px
PICKUP_RADIUS1 = 8  # px
PICKUP_RADIUS2 = 16  # px


class PickUp(Particle):
    def __init__(self, pos: pr.Vector2, dir: pr.Vector2, item: Item, target: Character):
        super().__init__(pos)
        self.item = item
        self.target = target
        self.texture = load_texture(item.texture)
        self.force = pr.vector2_scale(pr.vector2_normalize(dir), PICKUP_FORCE_INITIAL)
        self.time = 0

    def play_sound_effect(self) -> None:
        if pr.vector2_distance(self.pos, self.target.pos) < PICKUP_RADIUS2 and self.time >= 1.0:
            play_sound("pick")

    def update(self, dt: float):
        self.time += dt
        self.life = 100

        if 0.5 <= self.time < 1.0:
            self.vel = pr.vector2_zero()
        elif self.time >= 1.0:
            self.seek(self.target.pos, PICKUP_FORCE_SEEK, PICKUP_RADIUS2)

            if pr.vector2_distance(self.pos, self.target.pos) < PICKUP_RADIUS1:
                self.target.inventory.append(self.item)
                self.life = 0

        super().update(dt)

    def draw(self):
        self.play_sound_effect()

        if self.time < 1.2:
            size = PICKUP_WIDTH * abs(math.sin(self.time * math.pi / 2))
            width, height = size * math.sin(self.time * math.pi * 2), size
        else:
            size = PICKUP_WIDTH * 0.1
            width, height = size, size

        pr.draw_texture_pro(
            self.texture,
            (0, 0, 32 if width >= 0 else -32, 32),
            (self.pos.x - abs(width) * 0.5, self.pos.y - abs(height) * 0.5, abs(width), abs(height)),
            (0, 0),
            0,
            pr.WHITE,
        )

        if DEBUG_ENABLED:
            pr.draw_circle_lines_v(self.target.pos, PICKUP_RADIUS1, pr.GREEN)
            pr.draw_circle_lines_v(self.target.pos, PICKUP_RADIUS2, pr.GREEN)

import math

import pyray as pr

from tinyrpg.constants import DEBUG_ENABLED
from tinyrpg.engine import Character, Item, Particle
from tinyrpg.engine.base.resources import load_texture
from tinyrpg.engine.base.sound import play_sound

PICKUP_SPEED_INITIAL = 100  # m.s-1
PICKUP_MAX_FORCE_SEEK = 1100  # N
PICKUP_WIDTH = 16  # px
PICKUP_RADIUS1 = 8  # px
PICKUP_RADIUS2 = 16  # px


class PickUp(Particle):
    def __init__(self, pos: pr.Vector2, dir: pr.Vector2, item: Item, target: Character):
        super().__init__(pos)
        self.item = item
        self.target = target
        self.texture = load_texture(item.texture)
        self.vel = pr.vector2_scale(pr.vector2_normalize(dir), PICKUP_SPEED_INITIAL)
        self.time = 0

    def play_sound_effect(self) -> None:
        if pr.vector2_distance(self.pos, self.target.pos) < PICKUP_RADIUS2 and self.time >= 1.0:
            play_sound("pick")

    def update(self, dt: float):
        self.time += dt
        self.life = 100

        if self.time < 1:
            self.gravity()
        elif self.time < 1.1:
            self.vel = pr.vector2_zero()
        else:
            self.seek(self.target.pos, PICKUP_MAX_FORCE_SEEK, PICKUP_RADIUS2)
            if pr.vector2_distance(self.pos, self.target.pos) < PICKUP_RADIUS1 and self.target.inventory:
                self.target.inventory.append(self.item)
                self.life = 0

        super().update(dt)

    def draw(self):
        self.play_sound_effect()

        alpha = abs(math.sin(self.time * math.pi / 2)) if self.time < 1 else 1
        size = PICKUP_WIDTH * (1 - alpha) + PICKUP_WIDTH * 0.5 * alpha

        pr.draw_texture_pro(
            self.texture,
            (0, 0, 32, 32),
            (self.pos.x - size * 0.5, self.pos.y - size * 0.5, size, size),
            (0, 0),
            0,
            pr.WHITE,
        )

        if DEBUG_ENABLED:
            pr.draw_circle_lines_v(self.target.pos, PICKUP_RADIUS1, pr.GREEN)
            pr.draw_circle_lines_v(self.target.pos, PICKUP_RADIUS2, pr.GREEN)

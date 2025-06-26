import math

import pyray as pr

from tinyrpg.engine import Character, Item, Particle
from tinyrpg.engine.base.renderer import CircleRenderer
from tinyrpg.resources import load_sound, load_texture

PICKUP_FORCE_INITIAL = 5000  # N
PICKUP_FORCE_SEEK = 1000  # N
PICKUP_WIDTH = 16  # px
PICKUP_RADIUS1 = 4  # px
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
        if (
            pr.vector2_distance(self.pos, self.target.pos) < PICKUP_RADIUS2
            and self.time >= 1.0
            and not pr.is_sound_playing(load_sound("pick"))
        ):
            pr.play_sound(load_sound("pick"))

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

        if self.time < 2.0:
            size = PICKUP_WIDTH * abs(math.sin(self.time * math.pi / 2))
        else:
            size = PICKUP_WIDTH * 0.1

        pr.draw_circle_v(self.pos, size * 0.75, pr.color_alpha(pr.WHITE, 0.5))
        pr.draw_texture_pro(
            self.texture,
            (0, 0, 32, 32),
            (self.pos.x - size * 0.5, self.pos.y - size * 0.5, size, size),
            (0, 0),
            0,
            pr.WHITE,
        )

        CircleRenderer(self.target.pos, PICKUP_RADIUS1).draw()
        CircleRenderer(self.target.pos, PICKUP_RADIUS2).draw()

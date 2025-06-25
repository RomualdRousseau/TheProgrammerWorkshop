import math

import pyray as pr

from tinyrpg.engine import Character, Item, Particle
from tinyrpg.resources import load_sound, load_texture

PICKUP_WIDTH = 16


class PickUp(Particle):
    def __init__(self, pos: pr.Vector2, dir: pr.Vector2, item: Item, target: Character):
        super().__init__(pos)
        self.item = item
        self.target = target
        self.texture = load_texture(item.texture)
        self.time = 0
        self.force = pr.vector2_scale(pr.vector2_normalize(dir), 5000)

    def play_sound_effect(self) -> None:
        if (
            pr.vector2_distance(self.pos, self.target.pos) < 5
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
            self.seek(self.target.pos, 1000, 10)
            if pr.vector2_distance(self.pos, self.target.pos) < 5:
                self.target.inventory.append(self.item)
                self.life = 0

        super().update(dt)

    def draw(self):
        self.play_sound_effect()
        if self.time < 2.0:
            zoom = abs(math.sin(self.time * math.pi / 2))
        else:
            zoom = 0.1
        size = PICKUP_WIDTH * zoom
        pr.draw_circle_v(self.pos, size * 0.75, pr.color_alpha(pr.WHITE, 0.1))
        pr.draw_texture_pro(
            self.texture,
            (0, 0, 32, 32),
            (self.pos.x - size * 0.5, self.pos.y - size * 0.5, size, size),
            (0, 0),
            0,
            pr.color_alpha(pr.WHITE, 0.9),
        )

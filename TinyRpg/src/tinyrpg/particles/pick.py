import math

import pyray as pr

from tinyrpg.engine import Character, Item, Particle
from tinyrpg.resources import load_sound, load_texture


class Pick(Particle):
    def __init__(self, pos: pr.Vector2, item: Item, target: Character):
        super().__init__(pos)
        self.item = item
        self.target = target
        self.texture = load_texture(item.texture)
        self.time = 0
        self.random_force(5000, 0, math.pi)

    def play_sound_effect(self) -> None:
        if pr.vector2_distance(self.pos, self.target.pos) < 5 and not pr.is_sound_playing(load_sound("pick")):
            pr.play_sound(load_sound("pick"))

    def update(self, dt: float):
        self.time += dt
        self.life = 100

        if self.time >= 0.5:
            self.seek(self.target.pos, 1000, 10)
            if pr.vector2_distance(self.pos, self.target.pos) < 5:
                self.target.inventory.append(self.item)
                self.life = 0

        super().update(dt)

    def draw(self):
        self.play_sound_effect()
        pr.draw_texture_pro(self.texture, (0, 0, 32, 32), (self.pos.x, self.pos.y, 8, 8), (0, 0), 0, pr.WHITE)

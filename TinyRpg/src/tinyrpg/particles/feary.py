import math

import pyray as pr

from tinyrpg.engine import Character, Item, Particle
from tinyrpg.resources import load_sound, load_texture


class Feary(Particle):
    def __init__(self, name: str, pos: pr.Vector2, target: Character, item: Item):
        super().__init__(pos)
        self.texture = load_texture(name)
        self.target = target
        self.item = item
        self.time = 0
        self.random_force(5000, 0, math.pi)

    def play_sound_effect(self) -> None:
        if self.time == 0 and not pr.is_sound_playing(load_sound("step")):
            pr.play_sound(load_sound("step"))

    def update(self, dt: float):
        self.time += dt
        self.life = 100

        if self.time > 0.5:
            self.seek(self.target.pos, 1000, 10)
            if pr.vector2_distance(self.pos, self.target.pos) < 5:
                self.target.inventory.append(self.item)
                self.life = 0

        super().update(dt)

    def draw(self):
        self.play_sound_effect()
        pr.draw_texture_pro(self.texture, (0, 0, 32, 32), (self.pos.x, self.pos.y, 8, 8), (0, 0), 0, pr.WHITE)

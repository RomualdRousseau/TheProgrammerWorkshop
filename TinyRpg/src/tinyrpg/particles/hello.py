import pyray as pr

from tinyrpg.engine.draw_command import DrawMessage, DrawRectangle
from tinyrpg.engine.draw_manager import emit_draw_command
from tinyrpg.engine.particle import Particle


class Hello(Particle):
    def __init__(self, pos: pr.Vector2, greeting: str):
        super().__init__(pos)
        self.greeting = greeting

    def update(self, dt: float):
        super().update(dt)

    def draw(self):
        if self.life >= (100 - 15):
            time = (self.life - (100 - 15)) / 15
            size = pr.measure_text(self.greeting, 10)
            w1, w2 = 9 * time, 9 * (1 - time)
            rect = pr.Rectangle(self.pos.x - 4, self.pos.y - 4 + w1, size + 8, w2 * 2)
            emit_draw_command(DrawRectangle(99, rect, pr.RAYWHITE, pr.BLUE))
        elif self.life > 15:
            emit_draw_command(
                DrawMessage(
                    99,
                    self.greeting,
                    self.pos,
                    pr.RAYWHITE,
                    pr.BLUE,
                )
            )
        else:
            time = self.life / 15
            size = pr.measure_text(self.greeting, 10)
            w1, w2 = 9 * (1 - time), 9 * time
            rect = pr.Rectangle(self.pos.x - 4, self.pos.y - 4 + w1, size + 8, w2 * 2)
            emit_draw_command(DrawRectangle(99, rect, pr.RAYWHITE, pr.BLUE))

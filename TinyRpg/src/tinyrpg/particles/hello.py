import pyray as pr

from tinyrpg.engine.draw_command import DrawText
from tinyrpg.engine.draw_manager import emit_draw_command
from tinyrpg.engine.particle import Particle


class Hello(Particle):
    def __init__(self, pos: pr.Vector2):
        super().__init__(pos)
        self.vel = pr.Vector2(0, -30)

    def update(self, dt: float):
        super().update(dt)

    def draw(self):
        emit_draw_command(
            DrawText(
                99,
                "Hello, How are you?",
                self.pos,
                pr.color_alpha(pr.RAYWHITE, self.life / 100),
                pr.color_alpha(pr.BLACK, self.life / 100),
            )
        )

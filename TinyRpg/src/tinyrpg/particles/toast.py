import pyray as pr

from tinyrpg.engine.drawing import draw_text_outlined_v
from tinyrpg.engine.particle import Particle
from tinyrpg.engine.renderer import renderer_unsorted_draw


class Toast(Particle):
    def __init__(self, pos: pr.Vector2, text: str):
        super().__init__(pos)
        self.vel = pr.Vector2(0, -20)
        self.text = text
        self.font_size = 10

    def update(self, dt: float):
        super().update(dt)

    @renderer_unsorted_draw
    def draw(self):
        fg_color, bg_color = (
            pr.color_alpha(pr.RAYWHITE, self.life / 100),
            pr.color_alpha(pr.BLACK, self.life / 100),
        )
        draw_text_outlined_v(self.text, self.pos, self.font_size, fg_color, bg_color)

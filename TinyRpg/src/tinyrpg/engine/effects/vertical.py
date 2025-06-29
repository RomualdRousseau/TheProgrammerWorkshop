import pyray as pr

from tinyrpg.engine import Widget
from tinyrpg.engine.base.resources import load_texture
from tinyrpg.engine.gui.window import WINDOW_BORDER

WINDOW_FADE_SPEED = 2  # px.s-1


class VerticalEffect(Widget):
    def __init__(self, widget: Widget):
        super().__init__(widget.pos, widget.size)
        self.widget = widget
        self.state = 0
        self.fade_time = 0
        self.texture = load_texture("skin-gui")
        self.textureNPatch = pr.NPatchInfo(
            pr.Rectangle(0, 0, 32, 32),
            WINDOW_BORDER,
            WINDOW_BORDER,
            WINDOW_BORDER,
            WINDOW_BORDER,
            pr.NPatchLayout.NPATCH_NINE_PATCH,
        )

    def update(self, dt: float):
        match self.state:
            case 0:
                self.fade_time += WINDOW_FADE_SPEED * dt
                if self.fade_time >= 1:
                    self.fade_time = 1
                    self.state = 1
            case 1:
                self.widget.update(dt)
                if self.widget.closed:
                    self.state = 2
            case 2:
                self.fade_time -= WINDOW_FADE_SPEED * dt
                if self.fade_time <= 0:
                    self.fade_time = 0
                    self.state = 3
            case 3:
                self.close()
        super().update(dt)

    def draw(self):
        if self.state == 1:
            self.widget.draw()
        elif self.state in (0, 2):
            rect = self.get_rect()
            rect.y += rect.height * (1 - self.fade_time) // 2
            rect.height = rect.height * self.fade_time

            pr.draw_texture_n_patch(
                self.texture, self.textureNPatch, rect, (0, 0), 0, pr.color_alpha(pr.WHITE, self.fade_time)
            )

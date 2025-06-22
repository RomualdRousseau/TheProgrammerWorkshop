import pyray as pr

from tinyrpg.engine import Widget

MESSAGE_HEIGHT = 200  # px
MESSAGE_BORDER = 1  # px
MESSAGE_MARGIN = 5  # px
MESSAGE_PADDING = 2  # px
MESSAGE_FONT_SIZE = 10  # px
MESSAGE_FONT_SPACE = 2  # px
MESSAGE_FADE_SPEED = 2  # px.s-1
MESSAGE_STROKE_SPEED = 45  # ch.s-1
MESSAGE_PORTRAIT_SIZE = 64  # px


class VerticalEffect(Widget):
    def __init__(self, widget: Widget):
        super().__init__(widget.pos, widget.size)
        self.widget = widget
        self.state = 0
        self.fade_time = 0

    def update(self, dt: float):
        match self.state:
            case 0:
                self.fade_time += MESSAGE_FADE_SPEED * dt
                if self.fade_time >= 1:
                    self.fade_time = 1
                    self.state = 1
            case 1:
                self.widget.update(dt)
                if self.widget.closed:
                    self.state = 2
            case 2:
                self.fade_time -= MESSAGE_FADE_SPEED * dt
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

            pr.draw_rectangle_rec(rect, pr.color_alpha(pr.BLUE, self.fade_time * 0.8))
            pr.draw_rectangle_lines_ex(rect, MESSAGE_BORDER, pr.color_alpha(pr.RAYWHITE, self.fade_time))

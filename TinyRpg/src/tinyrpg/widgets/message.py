import pyray as pr

from tinyrpg.constants import WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine.widget import Widget

MESSAGE_HEIGHT = 50  # px
MESSAGE_BORDER = 1  # px
MESSAGE_MARGIN = 5  # px
MESSAGE_PADDING = 2  # px
MESSAGE_FONT_SIZE = 10  # px
MESSAGE_FONT_SPACE = 2  # px
MESSAGE_FADE_SPEED = 8  # px.s-1
MESSAGE_STROKE_SPEED = 45  # ch.s-1


class Message(Widget):
    def __init__(self, name: str, text: str, camera: pr.Camera2D):
        pos = pr.Vector2(MESSAGE_MARGIN, WORLD_HEIGHT - MESSAGE_HEIGHT - MESSAGE_MARGIN)
        size = pr.Vector2(WORLD_WIDTH - MESSAGE_MARGIN * 2, MESSAGE_HEIGHT)
        super().__init__(pos, size)

        self.name = name
        self.text = text
        self.camera = camera
        self.state = 0
        self.fade_time = 0
        self.stroke_time = 0

    def handle_input(self):
        if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
            self.state = 2

    def update(self, dt: float):
        match self.state:
            case 0:
                self.fade_time += MESSAGE_FADE_SPEED * dt
                if self.fade_time >= 1:
                    self.fade_time = 1
                    self.state = 1
            case 1:
                self.handle_input()
                self.stroke_time = min(self.stroke_time + MESSAGE_STROKE_SPEED * dt, len(self.text))
            case 2:
                self.fade_time -= MESSAGE_FADE_SPEED * dt
                if self.fade_time <= 0:
                    self.fade_time = 0
                    self.state = 3
            case 3:
                self.close()
        super().update(dt)

    def draw(self):
        rect = self.get_rect_2d(self.camera)
        rect.y += rect.height * (1 - self.fade_time) // 2
        rect.height = rect.height * self.fade_time

        pr.draw_rectangle_rec(rect, pr.color_alpha(pr.BLUE, 0.8))
        pr.draw_rectangle_lines_ex(rect, MESSAGE_BORDER, pr.RAYWHITE)

        if self.state == 1:
            pr.draw_text(
                self.name, int(rect.x + MESSAGE_PADDING), int(rect.y + MESSAGE_PADDING), MESSAGE_FONT_SIZE, pr.RAYWHITE
            )
            pr.draw_text(
                self.text[: int(self.stroke_time)],
                int(rect.x + MESSAGE_PADDING),
                int(rect.y + MESSAGE_FONT_SIZE + MESSAGE_PADDING + MESSAGE_FONT_SPACE),
                MESSAGE_FONT_SIZE,
                pr.RAYWHITE,
            )

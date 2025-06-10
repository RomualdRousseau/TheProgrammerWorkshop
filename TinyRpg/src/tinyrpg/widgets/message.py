import pyray as pr

from tinyrpg.constants import WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine.widget import Widget
from tinyrpg.resources import load_sound, load_texture

MESSAGE_HEIGHT = 50  # px
MESSAGE_BORDER = 1  # px
MESSAGE_MARGIN = 5  # px
MESSAGE_PADDING = 2  # px
MESSAGE_FONT_SIZE = 10  # px
MESSAGE_FONT_SPACE = 2  # px
MESSAGE_FADE_SPEED = 8  # px.s-1
MESSAGE_STROKE_SPEED = 45  # ch.s-1
MESSAGE_PORTRAIT_SIZE = 64  # px


class MessageBox(Widget):
    def __init__(self, name: str, portrait: str, text: str):
        super().__init__(
            pr.Vector2(MESSAGE_MARGIN, WORLD_HEIGHT - MESSAGE_HEIGHT - MESSAGE_MARGIN),
            pr.Vector2(WORLD_WIDTH - MESSAGE_MARGIN * 2, MESSAGE_HEIGHT),
        )

        self.name = name
        self.text = text
        self.portrait = load_texture(portrait)

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
        if self.stroke_time < len(self.text):
            if not pr.is_sound_playing(load_sound("key")):
                pr.play_sound(load_sound("key"))
        else:
            pr.stop_sound(load_sound("key"))

        rect = self.get_rect()
        rect.y += rect.height * (1 - self.fade_time) // 2
        rect.height = rect.height * self.fade_time

        pr.draw_rectangle_rec(rect, pr.color_alpha(pr.BLUE, self.fade_time * 0.8))
        pr.draw_rectangle_lines_ex(rect, MESSAGE_BORDER, pr.color_alpha(pr.RAYWHITE, self.fade_time))

        if self.state == 1:
            name_width = pr.measure_text(self.name, MESSAGE_FONT_SIZE)
            pr.draw_rectangle_v(
                (rect.x, rect.y - MESSAGE_FONT_SIZE),
                (name_width + MESSAGE_PADDING * 3, MESSAGE_FONT_SIZE),
                pr.RAYWHITE,
            )
            pr.draw_text(
                self.name,
                int(rect.x + MESSAGE_PADDING),
                int(rect.y - MESSAGE_FONT_SIZE + 1),
                MESSAGE_FONT_SIZE,
                pr.BLUE,
            )
            pr.draw_text(
                self.text[: int(self.stroke_time)],
                int(rect.x + MESSAGE_PADDING),
                int(rect.y + MESSAGE_PADDING),
                MESSAGE_FONT_SIZE,
                pr.RAYWHITE,
            )
            pr.draw_texture_pro(
                self.portrait,
                pr.Rectangle(0, 0, self.portrait.width, self.portrait.height),
                pr.Rectangle(
                    rect.x + rect.width - MESSAGE_PORTRAIT_SIZE - MESSAGE_BORDER,
                    rect.y + rect.height - MESSAGE_PORTRAIT_SIZE - MESSAGE_BORDER,
                    MESSAGE_PORTRAIT_SIZE,
                    MESSAGE_PORTRAIT_SIZE,
                ),
                pr.vector2_zero(),
                0.0,
                pr.WHITE,
            )

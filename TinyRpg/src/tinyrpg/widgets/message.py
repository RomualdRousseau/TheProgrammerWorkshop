import pyray as pr

from tinyrpg.constants import INPUT_CLOSE_MESSAGE, WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine import Widget, is_key_pressed
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
        self.stroke_time = 0

    def handle_input(self):
        if is_key_pressed(INPUT_CLOSE_MESSAGE):
            self.close()

    def play_sound_effect(self):
        if self.stroke_time < len(self.text):
            if not pr.is_sound_playing(load_sound("key")):
                pr.play_sound(load_sound("key"))
        else:
            pr.stop_sound(load_sound("key"))

    def update(self, dt: float):
        self.handle_input()
        self.stroke_time = min(self.stroke_time + MESSAGE_STROKE_SPEED * dt, len(self.text))
        super().update(dt)

    def draw(self):
        self.play_sound_effect()
        rect = self.get_rect()

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

        pr.draw_rectangle_rec(rect, pr.color_alpha(pr.BLUE, 0.8))
        pr.draw_rectangle_lines_ex(rect, MESSAGE_BORDER, pr.RAYWHITE)

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

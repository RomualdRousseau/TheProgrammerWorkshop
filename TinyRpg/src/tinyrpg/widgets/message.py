import pyray as pr

from tinyrpg.constants import INPUT_MESSAGE_NEXT, WORLD_HEIGHT
from tinyrpg.engine import ImageBox, TableLayout, TextBox, TitlePosition, Window, WindowLocation, is_action_pressed
from tinyrpg.resources import load_sound, load_texture

MESSAGE_HEIGHT = int(WORLD_HEIGHT * 0.3)  # px
MESSAGE_FONT_SIZE = 10  # px
MESSAGE_FONT_SPACE = 2  # px
MESSAGE_FADE_SPEED = 8  # px.s-1
MESSAGE_STROKE_SPEED = 45  # ch.s-1


class MessageBox(Window):
    def __init__(self, name: str, portrait: str, text: str):
        super().__init__(MESSAGE_HEIGHT, WindowLocation.BOTTOM, name, TitlePosition.LEFT)
        self.text = text
        self.stroke_time = 0
        self.text_box = TextBox("")

        self.add(
            TableLayout(1, 2).add(self.text_box).add(ImageBox(load_texture(portrait)).set_fixed_width(MESSAGE_HEIGHT))
        ).pack()

    def handle_input(self):
        if is_action_pressed(INPUT_MESSAGE_NEXT):
            self.close()

    def update_text_stroke(self, dt: float):
        self.stroke_time = min(self.stroke_time + MESSAGE_STROKE_SPEED * dt, len(self.text))
        self.text_box.text = self.text[: int(self.stroke_time)]

    def play_sound_effect(self):
        if self.stroke_time < len(self.text):
            if not pr.is_sound_playing(load_sound("key")):
                pr.play_sound(load_sound("key"))
        else:
            pr.stop_sound(load_sound("key"))

    def update(self, dt: float):
        self.handle_input()
        self.update_text_stroke(dt)
        super().update(dt)

    def draw(self):
        self.play_sound_effect()
        super().draw()

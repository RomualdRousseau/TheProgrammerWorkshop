import pyray as pr

from tinyrpg.constants import INPUT_MESSAGE_NEXT, WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine import (
    ImageBox,
    TableLayout,
    TextBox,
    TitlePosition,
    Window,
    WindowLocation,
    is_action_pressed,
    load_texture,
    play_sound,
    stop_sound,
)

MESSAGE_HEIGHT = int(WORLD_HEIGHT * 0.3)  # px
MESSAGE_FONT_SIZE = 10  # px
MESSAGE_FONT_SPACE = 2  # px
MESSAGE_FADE_SPEED = 8  # px.s-1
MESSAGE_STROKE_SPEED = 45  # ch.s-1
MESSAGE_LINE_COUNT = 4


class MessageBox(Window):
    def __init__(self, name: str, text: str):
        super().__init__(WORLD_WIDTH, MESSAGE_HEIGHT, WindowLocation.BOTTOM, name.upper(), TitlePosition.LEFT)
        self.text = [s for s in text.split("\n") if len(s) > 0]
        self.text_box = TextBox("")
        self.cursor = 0
        self.stroke_time = [0.0 for _ in range(len(self.text))]
        self.stroke_line = 0

        portrait = f"portrait-{name}".lower()
        self.add(
            TableLayout(1, 2).add(self.text_box).add(ImageBox(load_texture(portrait)).set_fixed_width(MESSAGE_HEIGHT))
        ).pack()

    def is_overflown(self):
        return len(self.text) > MESSAGE_LINE_COUNT

    def is_end_of_text(self):
        return self.cursor == (len(self.text) - MESSAGE_LINE_COUNT)

    def get_stroking_line(self):
        for i in range(len(self.text)):
            if self.stroke_time[i] < len(self.text[i]):
                return i
        return -1

    def handle_input(self):
        if is_action_pressed(INPUT_MESSAGE_NEXT):
            self.close()
        if self.is_overflown() and self.stroke_line < 0:
            if pr.is_key_pressed(pr.KeyboardKey.KEY_UP):
                self.cursor = max(self.cursor - 1, 0)
            if pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN):
                self.cursor = min(self.cursor + 1, len(self.text) - MESSAGE_LINE_COUNT)

    def update_text_stroke(self, dt: float):
        if self.stroke_line < 0:
            return

        self.stroke_line = self.get_stroking_line()
        if self.stroke_line >= 0:
            self.stroke_time[self.stroke_line] = min(
                self.stroke_time[self.stroke_line] + MESSAGE_STROKE_SPEED * dt, len(self.text[self.stroke_line])
            )
        if self.stroke_line >= self.cursor + MESSAGE_LINE_COUNT:
            self.cursor = min(self.cursor + 1, len(self.text) - MESSAGE_LINE_COUNT)

    def update_text_box(self):
        self.text_box.text = ""
        for i in range(self.cursor, min(self.cursor + MESSAGE_LINE_COUNT, len(self.text))):
            if self.stroke_line >= 0 and i == self.stroke_line:
                self.text_box.text += self.text[i][: int(self.stroke_time[i])]
                break
            else:
                self.text_box.text += self.text[i]
            self.text_box.text += "\n"

    def play_sound_effect(self):
        if self.stroke_line >= 0:
            play_sound("key")
        else:
            stop_sound("key")

    def update(self, dt: float):
        self.handle_input()
        self.update_text_stroke(dt)
        self.update_text_box()
        super().update(dt)

    def draw(self):
        self.play_sound_effect()
        super().draw()

import pyray as pr

from tinyrpg.constants import WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine import Widget, get_inventory

MESSAGE_HEIGHT = 200  # px
MESSAGE_BORDER = 1  # px
MESSAGE_MARGIN = 5  # px
MESSAGE_PADDING = 2  # px
MESSAGE_FONT_SIZE = 10  # px
MESSAGE_FONT_SPACE = 2  # px
MESSAGE_FADE_SPEED = 8  # px.s-1
MESSAGE_STROKE_SPEED = 45  # ch.s-1
MESSAGE_PORTRAIT_SIZE = 64  # px


class InventoryBox(Widget):
    def __init__(self):
        super().__init__(
            pr.Vector2(MESSAGE_MARGIN, WORLD_HEIGHT - MESSAGE_HEIGHT - MESSAGE_MARGIN),
            pr.Vector2(WORLD_WIDTH - MESSAGE_MARGIN * 2, MESSAGE_HEIGHT),
        )
        self.cursor = 0

    def handle_input(self):
        if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
            self.close()
        if pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN):
            self.cursor += 1
        if pr.is_key_pressed(pr.KeyboardKey.KEY_UP):
            self.cursor -= 1

    def update(self, dt: float):
        self.handle_input()
        super().update(dt)

    def draw(self):
        rect = self.get_rect()
        pr.draw_rectangle_rec(rect, pr.color_alpha(pr.BLUE, 0.8))
        pr.draw_rectangle_lines_ex(rect, MESSAGE_BORDER, pr.RAYWHITE)

        inventory = get_inventory()
        for y, item in enumerate(inventory.bag):
            symbol = "> " if y == self.cursor else "  "
            pr.draw_text(
                symbol + item.name,
                int(rect.x + MESSAGE_PADDING),
                int(rect.y + MESSAGE_PADDING + y * MESSAGE_FONT_SIZE),
                MESSAGE_FONT_SIZE,
                pr.RAYWHITE,
            )

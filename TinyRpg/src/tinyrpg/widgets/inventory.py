import pyray as pr

from tinyrpg.constants import WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine import Widget
from tinyrpg.resources import load_texture

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
        half_width = self.size.x // 2
        item_size = (half_width - MESSAGE_MARGIN) / 3 - MESSAGE_MARGIN
        item_offset = (half_width - MESSAGE_MARGIN) / 3
        x, y = rect.x + MESSAGE_MARGIN, rect.y + MESSAGE_MARGIN

        pr.draw_rectangle_rec(rect, pr.color_alpha(pr.BLUE, 0.8))
        pr.draw_rectangle_lines_ex(rect, MESSAGE_BORDER, pr.RAYWHITE)

        name_width = pr.measure_text("Romuald", 10)
        pr.draw_text(
            "Romuald",
            int(x + (half_width - 2 * MESSAGE_MARGIN - name_width) // 2),
            int(y),
            MESSAGE_FONT_SIZE,
            pr.RAYWHITE,
        )
        pr.draw_texture_pro(
            load_texture("hero"),
            pr.Rectangle(0, 0, 32, 32),
            pr.Rectangle(rect.x + (half_width - 64) // 2 + 1, y + item_offset + 2, 64, 64),
            pr.vector2_zero(),
            0,
            pr.WHITE,
        )
        y += MESSAGE_FONT_SIZE + MESSAGE_MARGIN

        for i in range(3):
            for j in range(3):
                if i == 0 and j == 1 or i == 2 and j == 0 or i == 2 and j == 2:
                    pr.draw_rectangle_lines_ex(
                        pr.Rectangle(
                            x + j * item_offset,
                            y + i * item_offset,
                            item_size,
                            item_size,
                        ),
                        1,
                        pr.RAYWHITE,
                    )
        y += 3 * item_offset

        pr.draw_rectangle_lines_ex(
            pr.Rectangle(
                x,
                y,
                half_width - 2 * MESSAGE_MARGIN,
                MESSAGE_HEIGHT - MESSAGE_MARGIN - (y - rect.y),
            ),
            1,
            pr.RAYWHITE,
        )
        pr.draw_text(
            "XP :\t\t\t\t1",
            int(x + MESSAGE_PADDING),
            int(y + MESSAGE_PADDING + MESSAGE_FONT_SIZE * 0),
            MESSAGE_FONT_SIZE - MESSAGE_FONT_SPACE,
            pr.RAYWHITE,
        )
        pr.draw_text(
            "HP :\t\t\t\t5/5",
            int(x + MESSAGE_PADDING),
            int(y + MESSAGE_PADDING + MESSAGE_FONT_SIZE * 1),
            MESSAGE_FONT_SIZE - MESSAGE_FONT_SPACE,
            pr.RAYWHITE,
        )
        pr.draw_text(
            "ATK:\t\t\t\t1",
            int(x + MESSAGE_PADDING),
            int(y + MESSAGE_PADDING + MESSAGE_FONT_SIZE * 2),
            MESSAGE_FONT_SIZE - MESSAGE_FONT_SPACE,
            pr.RAYWHITE,
        )
        pr.draw_text(
            "DEF:\t\t\t\t1",
            int(x + MESSAGE_PADDING),
            int(y + MESSAGE_PADDING + MESSAGE_FONT_SIZE * 3),
            MESSAGE_FONT_SIZE - MESSAGE_FONT_SPACE,
            pr.RAYWHITE,
        )
        pr.draw_text(
            "COIN:\t\t\t\t100",
            int(x + MESSAGE_PADDING),
            int(y + MESSAGE_PADDING + MESSAGE_FONT_SIZE * 4),
            MESSAGE_FONT_SIZE - MESSAGE_FONT_SPACE,
            pr.RAYWHITE,
        )

        x, y = rect.x + half_width + MESSAGE_MARGIN, rect.y + MESSAGE_MARGIN

        name_width = pr.measure_text("Inventory", 10)
        pr.draw_text(
            "Inventory",
            int(x + (half_width - 2 * MESSAGE_MARGIN - name_width) // 2),
            int(y),
            MESSAGE_FONT_SIZE,
            pr.RAYWHITE,
        )
        y += MESSAGE_FONT_SIZE + MESSAGE_MARGIN

        for i in range(3):
            for j in range(3):
                pr.draw_rectangle_lines_ex(
                    pr.Rectangle(
                        x + j * item_offset,
                        y + i * item_offset,
                        item_size,
                        item_size,
                    ),
                    1,
                    pr.RAYWHITE,
                )
        y += 3 * item_offset

        pr.draw_rectangle_lines_ex(
            pr.Rectangle(
                x,
                y,
                half_width - MESSAGE_MARGIN * 2,
                MESSAGE_HEIGHT - MESSAGE_MARGIN - (y - rect.y),
            ),
            1,
            pr.RAYWHITE,
        )
        pr.draw_text(
            "Potion\nRestore 20 HP",
            int(x + MESSAGE_PADDING),
            int(y + MESSAGE_PADDING),
            8,
            pr.RAYWHITE,
        )

        # inventory = get_inventory()
        # for y, item in enumerate(inventory.bag):
        #     symbol = "> " if y == self.cursor else "  "
        #     pr.draw_text(
        #         symbol + item.name,
        #         int(rect.x + MESSAGE_PADDING),
        #         int(rect.y + MESSAGE_PADDING + y * MESSAGE_FONT_SIZE),
        #         MESSAGE_FONT_SIZE,
        #         pr.RAYWHITE,
        #     )

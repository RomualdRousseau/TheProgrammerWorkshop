import pyray as pr

from tinyrpg.characters import get_hero
from tinyrpg.constants import (
    INPUT_INVENTORY_CLOSE,
    INPUT_INVENTORY_DROP,
    INPUT_INVENTORY_EQUIP,
    INPUT_INVENTORY_NEXT,
    INPUT_INVENTORY_PREVIOUS,
    INPUT_INVENTORY_UNEQUIP,
    WORLD_HEIGHT,
    WORLD_WIDTH,
)
from tinyrpg.engine import (
    EquipmentType,
    Widget,
    is_action_pressed,
)
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
        if is_action_pressed(INPUT_INVENTORY_NEXT):
            self.cursor = min(self.cursor + 1, 3 + 8)
        if is_action_pressed(INPUT_INVENTORY_PREVIOUS):
            self.cursor = max(self.cursor - 1, 0)
        if is_action_pressed(INPUT_INVENTORY_CLOSE):
            self.close()
        if is_action_pressed(INPUT_INVENTORY_EQUIP) and self.cursor >= 3:
            get_hero().inventory.equip(self.cursor - 3)
        if is_action_pressed(INPUT_INVENTORY_DROP) and self.cursor >= 3:
            get_hero().inventory.drop(self.cursor - 3)
        if is_action_pressed(INPUT_INVENTORY_UNEQUIP) and self.cursor < 3:
            get_hero().inventory.unequip(self.cursor)

    def update(self, dt: float):
        self.handle_input()
        super().update(dt)

    def draw(self):
        hero = get_hero()
        inventory = hero.inventory

        rect = self.get_rect()
        half_width = rect.width // 2
        item_size = (half_width - MESSAGE_MARGIN) / 3 - MESSAGE_MARGIN
        item_offset = (half_width - MESSAGE_MARGIN) / 3
        x, y = rect.x + MESSAGE_MARGIN, rect.y + MESSAGE_MARGIN
        selected = None

        pr.draw_rectangle_rec(rect, pr.color_alpha(pr.BLUE, 0.8))
        pr.draw_rectangle_lines_ex(rect, MESSAGE_BORDER, pr.RAYWHITE)

        name = f"{hero.name} - Lvl {hero.stats.xp}"
        name_width = pr.measure_text(name, 10)
        pr.draw_text(
            name,
            int(x + (half_width - 2 * MESSAGE_MARGIN - name_width) // 2),
            int(y),
            MESSAGE_FONT_SIZE,
            pr.RAYWHITE,
        )
        pr.draw_texture_pro(
            hero.texture,
            pr.Rectangle(0, 0, 32, 32),
            pr.Rectangle(rect.x + (half_width - 64) // 2 + 1, y + item_offset + 2, 64, 64),
            pr.vector2_zero(),
            0,
            pr.WHITE,
        )
        y += MESSAGE_FONT_SIZE + MESSAGE_MARGIN

        equipment = inventory.equipment[EquipmentType.CLOTHE.value]
        if self.cursor == EquipmentType.CLOTHE.value:
            pr.draw_rectangle_lines_ex(
                pr.Rectangle(
                    x + 1 * item_offset,
                    y + 0 * item_offset,
                    item_size,
                    item_size,
                ),
                1,
                pr.YELLOW,
            )
            selected = equipment
        else:
            pr.draw_rectangle_lines_ex(
                pr.Rectangle(
                    x + 1 * item_offset,
                    y + 0 * item_offset,
                    item_size,
                    item_size,
                ),
                1,
                pr.RAYWHITE,
            )
        if equipment:
            pr.draw_texture(
                load_texture(equipment.texture),
                int(x + 1 * item_offset + 1),
                int(y + 0 * item_offset + 1),
                pr.WHITE,
            )
        equipment = inventory.equipment[EquipmentType.WEAPON.value]
        if self.cursor == EquipmentType.WEAPON.value:
            pr.draw_rectangle_lines_ex(
                pr.Rectangle(
                    x + 0 * item_offset,
                    y + 2 * item_offset,
                    item_size,
                    item_size,
                ),
                1,
                pr.YELLOW,
            )
            selected = equipment
        else:
            pr.draw_rectangle_lines_ex(
                pr.Rectangle(
                    x + 0 * item_offset,
                    y + 2 * item_offset,
                    item_size,
                    item_size,
                ),
                1,
                pr.RAYWHITE,
            )
        if equipment:
            pr.draw_texture(
                load_texture(equipment.texture),
                int(x + 0 * item_offset + 1),
                int(y + 2 * item_offset + 1),
                pr.WHITE,
            )
        equipment = inventory.equipment[EquipmentType.SHIELD.value]
        if self.cursor == EquipmentType.SHIELD.value:
            pr.draw_rectangle_lines_ex(
                pr.Rectangle(
                    x + 2 * item_offset,
                    y + 2 * item_offset,
                    item_size,
                    item_size,
                ),
                1,
                pr.YELLOW,
            )
            selected = equipment
        else:
            pr.draw_rectangle_lines_ex(
                pr.Rectangle(
                    x + 2 * item_offset,
                    y + 2 * item_offset,
                    item_size,
                    item_size,
                ),
                1,
                pr.RAYWHITE,
            )
        if equipment:
            pr.draw_texture(
                load_texture(equipment.texture),
                int(x + 2 * item_offset + 1),
                int(y + 2 * item_offset + 1),
                pr.WHITE,
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
            f"HP :\t\t\t\t{hero.health}/{hero.stats.hp}",
            int(x + MESSAGE_PADDING),
            int(y + MESSAGE_PADDING + MESSAGE_FONT_SIZE * 0),
            MESSAGE_FONT_SIZE - MESSAGE_FONT_SPACE,
            pr.RAYWHITE,
        )
        pr.draw_text(
            f"ATK:\t\t\t\t{hero.get_damage()}",
            int(x + MESSAGE_PADDING),
            int(y + MESSAGE_PADDING + MESSAGE_FONT_SIZE * 1),
            MESSAGE_FONT_SIZE - MESSAGE_FONT_SPACE,
            pr.RAYWHITE,
        )
        pr.draw_text(
            f"DEF:\t\t\t\t{hero.get_armor()}",
            int(x + MESSAGE_PADDING),
            int(y + MESSAGE_PADDING + MESSAGE_FONT_SIZE * 2),
            MESSAGE_FONT_SIZE - MESSAGE_FONT_SPACE,
            pr.RAYWHITE,
        )
        pr.draw_text(
            f"COIN:\t\t\t\t{inventory.coin}",
            int(x + MESSAGE_PADDING),
            int(y + MESSAGE_PADDING + MESSAGE_FONT_SIZE * 3),
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
                cursor = max(self.cursor - 3, -1)
                if cursor == i * 3 + j:
                    selected = inventory.bag[cursor]
                    pr.draw_rectangle_lines_ex(
                        pr.Rectangle(
                            x + j * item_offset,
                            y + i * item_offset,
                            item_size,
                            item_size,
                        ),
                        1,
                        pr.YELLOW,
                    )
                else:
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
                item = inventory.bag[i * 3 + j]
                if item:
                    pr.draw_texture(
                        load_texture(item.texture),
                        int(x + j * item_offset + 1),
                        int(y + i * item_offset + 1),
                        pr.WHITE,
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
        if selected:
            pr.draw_text(
                f"{selected.name}\n{selected.description}",
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

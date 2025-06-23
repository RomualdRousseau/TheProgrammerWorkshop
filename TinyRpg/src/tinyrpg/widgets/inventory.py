import math

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
    COMPONENT_PADDING,
    TEXTBOX_FONT_SIZE_DEFAULT,
    WINDOW_BORDER,
    WINDOW_MARGIN,
    WINDOW_PADDING,
    ImageBox,
    Panel,
    TableLayout,
    TextBox,
    TextBoxAlign,
    Window,
    WindowLocation,
    is_action_pressed,
)
from tinyrpg.engine.gui.item_box import ItemBox
from tinyrpg.resources import load_texture

INVENTORY_HEIGHT = int(WORLD_HEIGHT * 0.8)  # px
INVENTORY_TEXT_HEIGHT = TEXTBOX_FONT_SIZE_DEFAULT + COMPONENT_PADDING * 2
INVENTORY_ICON_HEIGHT = (WORLD_WIDTH - 2 * WINDOW_MARGIN - 2 * WINDOW_PADDING - 2 * WINDOW_BORDER) / 6
MESSAGE_PORTRAIT_SIZE = 64  # px


class InventoryBox(Window):
    def __init__(self):
        super().__init__(INVENTORY_HEIGHT, WindowLocation.MIDDLE)
        hero = get_hero()
        self.equipment_num = len(hero.inventory.equipment)
        self.cursor = self.equipment_num

        self.title = "Inventory"
        self.item_boxes: list[ItemBox] = []
        self.desc = TextBox("")

        equipments = TableLayout(1, self.equipment_num)
        for item in hero.inventory.equipment:
            item_box = ItemBox(item)
            equipments.add(item_box)
            self.item_boxes.append(item_box)

        stats = TableLayout(4, 2)
        stats.add(TextBox("HP:"))
        self.stats_hp = TextBox(f"{hero.health}/{hero.stats.hp}", align=TextBoxAlign.RIGHT)
        stats.add(self.stats_hp)
        stats.add(TextBox("DMG:"))
        self.stats_damage = TextBox(f"{hero.get_damage()}", align=TextBoxAlign.RIGHT)
        stats.add(self.stats_damage)
        stats.add(TextBox("ARM:"))
        self.stats_armor = TextBox(f"{hero.get_armor()}", align=TextBoxAlign.RIGHT)
        stats.add(self.stats_armor)
        stats.add(TextBox("COIN:"))
        self.stats_coin = TextBox(f"{hero.inventory.coin}", align=TextBoxAlign.RIGHT)
        stats.add(self.stats_coin)

        bag_rows = int(math.sqrt(len(hero.inventory.bag)))
        bag_cols = int(math.sqrt(len(hero.inventory.bag)))
        bag = TableLayout(bag_rows, bag_cols)
        for item in hero.inventory.bag:
            item_box = ItemBox(item)
            bag.add(item_box)
            self.item_boxes.append(item_box)

        self.add(
            TableLayout(1, 2)
            .add(
                (
                    TableLayout(5, 1)
                    .add(
                        TextBox(f"Romuald - Lvl {hero.stats.xp}", align=TextBoxAlign.CENTER).set_fixed_height(
                            INVENTORY_TEXT_HEIGHT
                        )
                    )
                    .add(
                        ImageBox(load_texture("player"), pr.Rectangle(0, 0, 32, 32)).set_fixed_height(
                            INVENTORY_ICON_HEIGHT * (bag_rows - 1)
                        )
                    )
                    .add(equipments.set_fixed_height(INVENTORY_ICON_HEIGHT))
                    .add(TextBox("Stats", align=TextBoxAlign.CENTER).set_fixed_height(INVENTORY_TEXT_HEIGHT))
                    .add(Panel().add(stats))
                )
            )
            .add(
                (
                    TableLayout(3, 1)
                    .add(TextBox("Bag", align=TextBoxAlign.CENTER).set_fixed_height(INVENTORY_TEXT_HEIGHT))
                    .add(bag.set_fixed_height(INVENTORY_ICON_HEIGHT * bag_rows))
                    .add(Panel().add(self.desc))
                )
            )
        ).pack()

    def handle_input(self):
        if is_action_pressed(INPUT_INVENTORY_NEXT):
            self.cursor = min(self.cursor + 1, len(self.item_boxes) - 1)
        if is_action_pressed(INPUT_INVENTORY_PREVIOUS):
            self.cursor = max(self.cursor - 1, 0)
        if is_action_pressed(INPUT_INVENTORY_CLOSE):
            self.close()
        if is_action_pressed(INPUT_INVENTORY_EQUIP) and self.cursor >= self.equipment_num:
            get_hero().inventory.equip(self.cursor - 3)
        if is_action_pressed(INPUT_INVENTORY_DROP) and self.cursor >= self.equipment_num:
            get_hero().inventory.drop(self.cursor - 3)
        if is_action_pressed(INPUT_INVENTORY_UNEQUIP) and self.cursor < self.equipment_num:
            get_hero().inventory.unequip(self.cursor)

    def update_items(self):
        hero = get_hero()
        for i, item_box in enumerate(self.item_boxes):
            item_box.selected = self.cursor == i
            if item_box.selected:
                self.desc.text = f"{item_box.item.name}\n{item_box.item.description}" if item_box.item else ""

            if i < self.equipment_num:
                item_box.item = hero.inventory.equipment[i]
            else:
                item_box.item = hero.inventory.bag[i - self.equipment_num]

    def update_stats(self):
        hero = get_hero()
        self.stats_hp.text = f"{hero.health}/{hero.stats.hp}"
        self.stats_damage.text = f"{hero.get_damage()}"
        self.stats_armor.text = f"{hero.get_armor()}"
        self.stats_coin.text = f"{hero.inventory.coin}"

    def update(self, dt: float):
        self.handle_input()
        self.update_items()
        self.update_stats()
        super().update(dt)

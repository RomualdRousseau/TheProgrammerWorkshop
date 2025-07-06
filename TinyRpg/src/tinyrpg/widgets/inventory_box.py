import math
from enum import Enum, auto

import pyray as pr

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
    Character,
    ImageBox,
    ItemBox,
    Panel,
    TableLayout,
    TextBox,
    TextBoxAlign,
    Window,
    WindowLocation,
    is_action_pressed,
    load_texture,
    play_sound,
)

INVENTORY_HEIGHT = int(WORLD_HEIGHT * 0.8)  # px
INVENTORY_TEXT_HEIGHT = TEXTBOX_FONT_SIZE_DEFAULT + COMPONENT_PADDING * 2 + 1
INVENTORY_ICON_HEIGHT = (WORLD_WIDTH - 2 * WINDOW_MARGIN - 2 * WINDOW_PADDING - 2 * WINDOW_BORDER) / 6


class InventoryBoxAction(Enum):
    NONE = auto()
    EQUIPING = auto()
    UNEQUIPING = auto()
    DROPPING = auto()


class InventoryBox(Window):
    def __init__(self, player: Character):
        assert player.inventory is not None, "Inventory must exist"
        super().__init__(WORLD_WIDTH, INVENTORY_HEIGHT, WindowLocation.MIDDLE, "INVENTORY")

        self.player = player
        self.equipment_num = len(player.inventory.equipment)
        self.cursor = self.equipment_num
        self.inventory = player.inventory

        self.bag: list[ItemBox] = []
        self.desc = TextBox("")
        self.action = InventoryBoxAction.NONE

        equipments = TableLayout(1, self.equipment_num)
        for item in player.inventory.equipment:
            item_box = ItemBox(item)
            equipments.add(item_box)
            self.bag.append(item_box)

        stats = TableLayout(4, 2)
        stats.add(TextBox("HP:"))
        self.stats_hp = TextBox(f"{self.player.health}/{self.player.stats.hp}", align=TextBoxAlign.RIGHT)
        stats.add(self.stats_hp)
        stats.add(TextBox("DMG:"))
        self.stats_damage = TextBox(f"{self.player.get_damage()}", align=TextBoxAlign.RIGHT)
        stats.add(self.stats_damage)
        stats.add(TextBox("ARM:"))
        self.stats_armor = TextBox(f"{self.player.get_armor()}", align=TextBoxAlign.RIGHT)
        stats.add(self.stats_armor)
        stats.add(TextBox("COIN:"))
        self.stats_coin = TextBox(f"{self.inventory.coin}", align=TextBoxAlign.RIGHT)
        stats.add(self.stats_coin)

        bag_rows = int(math.sqrt(len(self.inventory.bag)))
        bag_cols = int(math.sqrt(len(self.inventory.bag)))
        bag_panel = TableLayout(bag_rows, bag_cols)
        for item in self.inventory.bag:
            item_box = ItemBox(item)
            bag_panel.add(item_box)
            self.bag.append(item_box)

        self.add(
            TableLayout(1, 2)
            .add(
                (
                    TableLayout(5, 1)
                    .add(
                        TextBox(f"Romuald - Lvl {player.stats.xp}", align=TextBoxAlign.CENTER).set_fixed_height(
                            INVENTORY_TEXT_HEIGHT
                        )
                    )
                    .add(
                        ImageBox(load_texture("skin-player"), pr.Rectangle(0, 0, 32, 32)).set_fixed_height(
                            INVENTORY_ICON_HEIGHT * (bag_rows - 1) * 0.9
                        )
                    )
                    .add(equipments.set_fixed_height(INVENTORY_ICON_HEIGHT))
                    .add(TextBox("STATS", align=TextBoxAlign.CENTER).set_fixed_height(INVENTORY_TEXT_HEIGHT))
                    .add(Panel().add(stats))
                )
            )
            .add(
                (
                    TableLayout(3, 1)
                    .add(TextBox("BAG", align=TextBoxAlign.CENTER).set_fixed_height(INVENTORY_TEXT_HEIGHT))
                    .add(bag_panel.set_fixed_height(INVENTORY_ICON_HEIGHT * bag_rows))
                    .add(Panel().add(self.desc))
                )
            )
        ).pack()

        self.update_items()

    def play_sound_effect(self) -> None:
        match self.action:
            case InventoryBoxAction.EQUIPING:
                play_sound("equip")
            case InventoryBoxAction.UNEQUIPING:
                play_sound("unequip")
            case InventoryBoxAction.DROPPING:
                play_sound("drop")

    def handle_input(self):
        self.action = InventoryBoxAction.NONE
        if is_action_pressed(INPUT_INVENTORY_NEXT):
            self.cursor = min(self.cursor + 1, len(self.bag) - 1)
        if is_action_pressed(INPUT_INVENTORY_PREVIOUS):
            self.cursor = max(self.cursor - 1, 0)
        if is_action_pressed(INPUT_INVENTORY_CLOSE):
            self.close()
        if is_action_pressed(INPUT_INVENTORY_EQUIP) and self.cursor >= self.equipment_num:
            self.inventory.equip(self.cursor - 3)
            self.action = InventoryBoxAction.EQUIPING
        if is_action_pressed(INPUT_INVENTORY_UNEQUIP) and self.cursor < self.equipment_num:
            self.inventory.unequip(self.cursor)
            self.action = InventoryBoxAction.UNEQUIPING
        if is_action_pressed(INPUT_INVENTORY_DROP) and self.cursor >= self.equipment_num:
            self.inventory.drop(self.cursor - 3)
            self.action = InventoryBoxAction.DROPPING

    def update_items(self):
        for i, item_box in enumerate(self.bag):
            item_box.selected = self.cursor == i
            if item_box.selected:
                self.desc.text = f"{item_box.item.name}\n{item_box.item.description}" if item_box.item else ""

            if i < self.equipment_num:
                item_box.item = self.inventory.equipment[i]
            else:
                item_box.item = self.inventory.bag[i - self.equipment_num]

    def update_stats(self):
        self.stats_hp.text = f"{self.player.health}/{self.player.stats.hp}"
        self.stats_damage.text = f"{self.player.get_damage()}"
        self.stats_armor.text = f"{self.player.get_armor()}"
        self.stats_coin.text = f"{self.inventory.coin}"

    def update(self, dt: float):
        self.handle_input()
        self.update_items()
        self.update_stats()
        super().update(dt)

    def draw(self):
        self.play_sound_effect()
        super().draw()

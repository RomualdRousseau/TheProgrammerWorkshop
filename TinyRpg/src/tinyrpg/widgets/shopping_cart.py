import math
from enum import Enum, auto
from random import choice

from tinyrpg.constants import (
    INPUT_SHOPPING_CART_BUY,
    INPUT_SHOPPING_CART_CLOSE,
    INPUT_SHOPPING_CART_NEXT,
    INPUT_SHOPPING_CART_PREVIOUS,
    INPUT_SHOPPING_CART_SELL,
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
    ItemBox,
    ItemList,
    Panel,
    TableLayout,
    TextBox,
    TextBoxAlign,
    Window,
    WindowLocation,
    get_database,
    get_inventory_item,
    is_action_pressed,
    play_sound,
)

SHOPPING_CART_HEIGHT = int(WORLD_HEIGHT * 0.8)  # px
SHOPPING_CART_TEXT_HEIGHT = TEXTBOX_FONT_SIZE_DEFAULT + COMPONENT_PADDING * 2 + 1
SHOPPING_CART_ICON_HEIGHT = (WORLD_WIDTH - 2 * WINDOW_MARGIN - 2 * WINDOW_PADDING - 2 * WINDOW_BORDER) / 6
SHOPPING_CART_SIZE = 3


class ShoppingCartAction(Enum):
    NONE = auto()
    BUYING = auto()
    SELLING = auto()
    MOVING = auto()
    CLOSING = auto()


class ShoppingCart(Window):
    def __init__(self, player: Character):
        assert player.inventory is not None, "Inventory must exist"
        super().__init__(WORLD_WIDTH, SHOPPING_CART_HEIGHT, WindowLocation.MIDDLE, "SHOP")

        self.player = player
        self.cursor = 0
        self.inventory = player.inventory
        self.cart: list[ItemList] = []
        self.bag: list[ItemBox] = []
        self.stats_coin = TextBox(f"{player.inventory.coin}", align=TextBoxAlign.LEFT)
        self.desc = TextBox("")
        self.action = ShoppingCartAction.NONE

        cart_panel = TableLayout(SHOPPING_CART_SIZE, 1)
        for _ in range(SHOPPING_CART_SIZE):
            item_key = choice(list(get_database().select_dict("items").keys()))
            item = get_inventory_item(item_key)
            item_box = ItemList(item)
            cart_panel.add(item_box)
            self.cart.append(item_box)

        bag_rows = int(math.sqrt(len(self.inventory.bag)))
        bag_cols = int(math.sqrt(len(self.inventory.bag)))
        bag = TableLayout(bag_rows, bag_cols)
        for item in self.inventory.bag:
            item_box = ItemBox(item)
            bag.add(item_box)
            self.bag.append(item_box)

        self.add(
            TableLayout(1, 2)
            .add(
                (
                    TableLayout(3, 1)
                    .add(TextBox("CART", align=TextBoxAlign.CENTER).set_fixed_height(SHOPPING_CART_TEXT_HEIGHT))
                    .add(cart_panel)
                    .add(
                        TableLayout(1, 2)
                        .add(TextBox("COIN:"))
                        .add(self.stats_coin)
                        .set_fixed_height(SHOPPING_CART_TEXT_HEIGHT)
                    )
                )
            )
            .add(
                (
                    TableLayout(3, 1)
                    .add(TextBox("BAG", align=TextBoxAlign.CENTER).set_fixed_height(SHOPPING_CART_TEXT_HEIGHT))
                    .add(bag.set_fixed_height(SHOPPING_CART_ICON_HEIGHT * bag_rows))
                    .add(Panel().add(self.desc))
                )
            )
        ).pack()

        self.update_items()

    def play_sound_effect(self):
        match self.action:
            case ShoppingCartAction.BUYING:
                play_sound("buy")
            case ShoppingCartAction.SELLING:
                play_sound("sell")
            case ShoppingCartAction.MOVING:
                play_sound("move-cursor")
            case ShoppingCartAction.CLOSING:
                play_sound("close")

    def buy_item(self, slot: int):
        cart_item = self.cart[slot].item
        if cart_item and cart_item.cost <= self.inventory.coin:
            self.inventory.append(cart_item)
            self.inventory.coin -= cart_item.cost
            self.cart[slot].item = None  # TODO: Put a new random item?

    def sell_item(self, slot: int):
        bag_item = self.bag[slot].item
        if bag_item:
            self.inventory.drop(slot)
            self.inventory.coin += bag_item.cost // 2

    def handle_input(self):
        self.action = ShoppingCartAction.NONE
        if is_action_pressed(INPUT_SHOPPING_CART_NEXT):
            self.cursor = min(self.cursor + 1, len(self.cart) + len(self.bag) - 1)
            self.action = ShoppingCartAction.MOVING
        if is_action_pressed(INPUT_SHOPPING_CART_PREVIOUS):
            self.cursor = max(self.cursor - 1, 0)
            self.action = ShoppingCartAction.MOVING
        if is_action_pressed(INPUT_SHOPPING_CART_CLOSE):
            self.close()
            self.action = ShoppingCartAction.CLOSING
        if is_action_pressed(INPUT_SHOPPING_CART_BUY) and self.cursor < SHOPPING_CART_SIZE:
            self.buy_item(self.cursor)
            self.action = ShoppingCartAction.BUYING
        if is_action_pressed(INPUT_SHOPPING_CART_SELL) and self.cursor >= SHOPPING_CART_SIZE:
            self.sell_item(self.cursor - SHOPPING_CART_SIZE)
            self.action = ShoppingCartAction.SELLING

    def update_items(self):
        for i, item_box in enumerate(self.cart + self.bag):
            item_box.selected = self.cursor == i
            if i >= SHOPPING_CART_SIZE:
                item_box.item = self.inventory.bag[i - SHOPPING_CART_SIZE]
                if item_box.selected:
                    self.desc.text = f"{item_box.item.name}\n{item_box.item.description}" if item_box.item else ""

    def update_stats(self):
        self.stats_coin.text = f"{self.inventory.coin}"

    def update(self, dt: float):
        self.action = "IDLE"
        self.handle_input()
        self.update_items()
        self.update_stats()
        super().update(dt)

    def draw(self):
        self.play_sound_effect()
        super().draw()

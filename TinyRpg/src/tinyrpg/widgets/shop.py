import math
from random import uniform

from tinyrpg.characters import get_hero
from tinyrpg.constants import (
    INPUT_SHOP_BAG_NEXT,
    INPUT_SHOP_BAG_PREVIOUS,
    INPUT_SHOP_CART_NEXT,
    INPUT_SHOP_CART_PREVIOUS,
    INPUT_SHOP_CLOSE,
    ITEM_DATABASE,
    WORLD_HEIGHT,
    WORLD_WIDTH,
)
from tinyrpg.engine import (
    COMPONENT_PADDING,
    TEXTBOX_FONT_SIZE_DEFAULT,
    WINDOW_BORDER,
    WINDOW_MARGIN,
    WINDOW_PADDING,
    Item,
    ItemBox,
    Panel,
    TableLayout,
    TextBox,
    TextBoxAlign,
    Window,
    WindowLocation,
    is_action_pressed,
)

SHOP_HEIGHT = int(WORLD_HEIGHT * 0.8)  # px
SHOP_TEXT_HEIGHT = TEXTBOX_FONT_SIZE_DEFAULT + COMPONENT_PADDING * 2 + 1
SHOP_ICON_HEIGHT = (WORLD_WIDTH - 2 * WINDOW_MARGIN - 2 * WINDOW_PADDING - 2 * WINDOW_BORDER) / 6


class ShopBox(Window):
    def __init__(self):
        super().__init__(SHOP_HEIGHT, WindowLocation.MIDDLE)
        hero = get_hero()
        self.cursor_cart = 0
        self.cursor_bag = 0

        self.title = "Shop"
        self.cart: list[ItemBox] = []
        self.bag: list[ItemBox] = []
        self.desc = TextBox("")

        cart_panel = TableLayout(5, 2)
        for _ in range(5):
            item = Item(*ITEM_DATABASE[int(uniform(0, len(ITEM_DATABASE)))])
            item_box = ItemBox(item)
            cart_panel.add(item_box.set_fixed_width((self.get_inner_rect().height - SHOP_TEXT_HEIGHT) / 5))
            cart_panel.add(TextBox(f"{item.name}\n{item.description}\nPrice: 100"))
            self.cart.append(item_box)

        bag_rows = int(math.sqrt(len(hero.inventory.bag)))
        bag_cols = int(math.sqrt(len(hero.inventory.bag)))
        bag = TableLayout(bag_rows, bag_cols)
        for item in hero.inventory.bag:
            item_box = ItemBox(item)
            bag.add(item_box)
            self.bag.append(item_box)

        self.add(
            TableLayout(1, 2)
            .add(
                (
                    TableLayout(2, 1)
                    .add(TextBox("Items", align=TextBoxAlign.CENTER).set_fixed_height(SHOP_TEXT_HEIGHT))
                    .add(cart_panel)
                )
            )
            .add(
                (
                    TableLayout(3, 1)
                    .add(TextBox("Bag", align=TextBoxAlign.CENTER).set_fixed_height(SHOP_TEXT_HEIGHT))
                    .add(bag.set_fixed_height(SHOP_ICON_HEIGHT * bag_rows))
                    .add(Panel().add(self.desc))
                )
            )
        ).pack()

    def handle_input(self):
        if is_action_pressed(INPUT_SHOP_CART_NEXT):
            self.cursor_cart = min(self.cursor_cart + 1, len(self.cart) - 1)
        if is_action_pressed(INPUT_SHOP_CART_PREVIOUS):
            self.cursor_cart = max(self.cursor_cart - 1, 0)
        if is_action_pressed(INPUT_SHOP_BAG_NEXT):
            self.cursor_bag = min(self.cursor_bag + 1, len(self.bag) - 1)
        if is_action_pressed(INPUT_SHOP_BAG_PREVIOUS):
            self.cursor_bag = max(self.cursor_bag - 1, 0)
        if is_action_pressed(INPUT_SHOP_CLOSE):
            self.close()

    def update_items(self):
        for i, item_box in enumerate(self.cart):
            item_box.selected = self.cursor_cart == i

        for i, item_box in enumerate(self.bag):
            item_box.selected = self.cursor_bag == i
            if item_box.selected:
                self.desc.text = f"{item_box.item.name}\n{item_box.item.description}" if item_box.item else ""

    def update(self, dt: float):
        self.handle_input()
        self.update_items()
        super().update(dt)

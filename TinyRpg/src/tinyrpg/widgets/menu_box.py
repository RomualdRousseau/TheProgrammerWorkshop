from tinyrpg.constants import (
    INPUT_MENU_BOX_NEXT,
    INPUT_MENU_BOX_PREVIOUS,
    WORLD_HEIGHT,
    WORLD_WIDTH,
)
from tinyrpg.engine import (
    COMPONENT_PADDING,
    TEXTBOX_FONT_SIZE_DEFAULT,
    WINDOW_BORDER,
    WINDOW_MARGIN,
    WINDOW_PADDING,
    ItemText,
    TableLayout,
    TextBoxAlign,
    Window,
    WindowLocation,
    is_action_pressed,
)

MENU_BOX_HEIGHT = int(WORLD_HEIGHT * 0.50)  # px
MENU_BOX_TEXT_HEIGHT = TEXTBOX_FONT_SIZE_DEFAULT + COMPONENT_PADDING * 2 + 1
SHOPPING_CART_ICON_HEIGHT = (WORLD_WIDTH - 2 * WINDOW_MARGIN - 2 * WINDOW_PADDING - 2 * WINDOW_BORDER) / 6


CART_SIZE = 3


class MenuBox(Window):
    def __init__(self):
        super().__init__(WORLD_WIDTH, MENU_BOX_HEIGHT, WindowLocation.MIDDLE)

        self.cursor = 0

        self.items = [
            ItemText("CONTINUE", align=TextBoxAlign.CENTER),
            ItemText("NEW GAME", align=TextBoxAlign.CENTER),
            ItemText("QUIT", align=TextBoxAlign.CENTER),
        ]

        self.add(TableLayout(3, 1).add(self.items[0]).add(self.items[1]).add(self.items[2])).pack()

    def play_sound_effect(self) -> None:
        pass

    def handle_input(self):
        if is_action_pressed(INPUT_MENU_BOX_NEXT):
            self.cursor = min(self.cursor + 1, 2)
        if is_action_pressed(INPUT_MENU_BOX_PREVIOUS):
            self.cursor = max(self.cursor - 1, 0)

    def update_items(self):
        for i, item_text in enumerate(self.items):
            item_text.selected = self.cursor == i

    def update(self, dt: float):
        self.handle_input()
        self.update_items()
        super().update(dt)

    def draw(self):
        self.play_sound_effect()
        super().draw()

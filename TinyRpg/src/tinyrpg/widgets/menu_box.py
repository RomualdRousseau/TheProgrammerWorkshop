import os
from enum import Enum, auto
from typing import Optional, Protocol

from tinyrpg.constants import (
    INPUT_MENU_BOX_NEXT,
    INPUT_MENU_BOX_PREVIOUS,
    INPUT_MENU_BOX_SELECT,
    WORLD_WIDTH,
)
from tinyrpg.engine import (
    COMPONENT_PADDING,
    ITEMTEXT_BORDER,
    TEXTBOX_FONT_SIZE_DEFAULT,
    WINDOW_BORDER,
    WINDOW_MARGIN,
    WINDOW_PADDING,
    ItemText,
    SceneEvent,
    TableLayout,
    TextBoxAlign,
    Window,
    WindowLocation,
    is_action_pressed,
    play_sound,
)

MENU_BOX_WIDTH = int(WORLD_WIDTH * 0.75)  # px
MENU_BOX_HEIGHT = int((WINDOW_BORDER + WINDOW_PADDING + ITEMTEXT_BORDER * 4) * 2)  # px
MENU_BOX_TEXT_HEIGHT = TEXTBOX_FONT_SIZE_DEFAULT + COMPONENT_PADDING * 2 + 1
SHOPPING_CART_ICON_HEIGHT = (WORLD_WIDTH - 2 * WINDOW_MARGIN - 2 * WINDOW_PADDING - 2 * WINDOW_BORDER) / 6


CART_SIZE = 3


class Menu(Protocol):
    first_use: bool
    events: list[SceneEvent]


class MenuItem(Enum):
    LOAD = auto()
    CONTINUE = auto()
    SAVE = auto()
    NEW = auto()
    QUIT = auto()


class MenuBoxAction(Enum):
    NONE = auto()
    SELECTING = auto()
    MOVING = auto()


class MenuBox(Window):
    def __init__(self, with_save: bool):
        self.cursor = 0
        self.items: dict[ItemText, MenuItem] = {}
        self.selected_item: Optional[MenuItem] = None
        self.action = MenuBoxAction.NONE

        if os.path.exists("saved/state.pkl"):
            self.items[ItemText("LOAD GAME", align=TextBoxAlign.CENTER)] = MenuItem.LOAD

        if with_save:
            self.items[ItemText("CONTINUE", align=TextBoxAlign.CENTER)] = MenuItem.CONTINUE
            self.items[ItemText("SAVE GAME", align=TextBoxAlign.CENTER)] = MenuItem.SAVE

        self.items[ItemText("NEW GAME", align=TextBoxAlign.CENTER)] = MenuItem.NEW
        self.items[ItemText("QUIT", align=TextBoxAlign.CENTER)] = MenuItem.QUIT

        super().__init__(
            MENU_BOX_WIDTH, MENU_BOX_HEIGHT + MENU_BOX_TEXT_HEIGHT * len(self.items), WindowLocation.MIDDLE
        )

        table_menu = TableLayout(len(self.items), 1)
        for item in self.items.keys():
            table_menu.add(item)
        self.add(table_menu).pack()

        self.update_items()

    def play_sound_effect(self) -> None:
        match self.action:
            case MenuBoxAction.SELECTING:
                play_sound("select", True)
            case MenuBoxAction.MOVING:
                play_sound("move-cursor")

    def handle_input(self):
        self.action = MenuBoxAction.NONE
        if is_action_pressed(INPUT_MENU_BOX_NEXT):
            self.cursor = min(self.cursor + 1, len(self.items) - 1)
            self.action = MenuBoxAction.MOVING
        if is_action_pressed(INPUT_MENU_BOX_PREVIOUS):
            self.cursor = max(self.cursor - 1, 0)
            self.action = MenuBoxAction.MOVING
        if is_action_pressed(INPUT_MENU_BOX_SELECT):
            if item := next((x for x in self.items.keys() if x.selected), None):
                self.selected_item = self.items[item]
                self.action = MenuBoxAction.SELECTING

    def update_items(self):
        for i, item_text in enumerate(self.items):
            item_text.selected = self.cursor == i

    def update(self, dt: float):
        self.handle_input()
        self.update_items()
        super().update(dt)
        self.play_sound_effect()

    def draw(self):
        # self.play_sound_effect()
        super().draw()

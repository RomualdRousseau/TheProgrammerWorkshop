from typing import Optional

import pyray as pr

from tinyrpg.engine import OBJECT_SIZE, Animation, Item, Object

CHEST_ANIMATIONS = lambda: {
    "Idle": Animation(pr.Vector2(0, 0), OBJECT_SIZE, 1, 0),
    "Open": Animation(pr.Vector2(0, 0), OBJECT_SIZE, 2, 5, repeat=False),
}


class Chest(Object):
    def __init__(self, pos: pr.Vector2, content: Optional[Item] = None, key: Optional[Item] = None) -> None:
        super().__init__("chest", pos, CHEST_ANIMATIONS(), content, key)

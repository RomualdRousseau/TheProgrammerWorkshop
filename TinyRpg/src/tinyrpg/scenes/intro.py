from typing import Any, Optional

import pyray as pr

from tinyrpg.engine import Scene


def init(previous_scene: Optional[Scene] = None):
    pass


def release():
    pass


def update(dt: float):
    pass


def draw():
    pr.clear_background(pr.BLUE)


def get_state_and_input() -> tuple[str, str]:
    if pr.is_key_pressed(pr.KeyboardKey.KEY_X):
        return ("intro", "keypress")
    else:
        return ("intro", "self")


def save_state() -> dict[str, Any]:
    return {}


def restore_state(state: dict[str, Any]):
    pass

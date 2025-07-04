from typing import Any, Optional

import pyray as pr

from tinyrpg.constants import INPUT_MENU_BOX_SELECT
from tinyrpg.engine import FixedCamera, Scene, SceneEvent, is_action_pressed, unload_resources
from tinyrpg.widgets import MenuBox

events: list[SceneEvent] = []


def next_event() -> Optional[SceneEvent]:
    return events.pop(0) if len(events) > 0 else None


def init(previous_scene: Optional[Scene] = None):
    global menu_box, fixed_camera
    menu_box = MenuBox()
    fixed_camera = FixedCamera()


def release():
    unload_resources()


def update(dt: float):
    if is_action_pressed(INPUT_MENU_BOX_SELECT):
        match menu_box.cursor:
            case 0:
                events.append(SceneEvent("load", ()))
                events.append(SceneEvent("change_scene", ("menu", "keypress")))
            case 1:
                events.append(SceneEvent("change_scene", ("menu", "keypress")))
            case 2:
                events.append(SceneEvent("quit", ()))
    menu_box.update(dt)


def draw():
    pr.clear_background(pr.RED)
    pr.begin_mode_2d(fixed_camera.camera)
    menu_box.draw()
    pr.end_mode_2d()


def save_state() -> dict[str, Any]:
    return {}


def restore_state(state: dict[str, Any]):
    pass

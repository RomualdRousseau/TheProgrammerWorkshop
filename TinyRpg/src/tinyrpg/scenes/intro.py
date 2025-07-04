from typing import Any, Optional

import pyray as pr

from tinyrpg.engine import Scene, SceneEvent, unload_resources

events: list[SceneEvent] = []


def next_event() -> Optional[SceneEvent]:
    return events.pop(0) if len(events) > 0 else None


def init(previous_scene: Optional[Scene] = None):
    pass


def release():
    unload_resources()


def update(dt: float):
    if pr.is_key_pressed(pr.KeyboardKey.KEY_X):
        events.append(SceneEvent("change_scene", ("intro", "keypress")))


def draw():
    pr.clear_background(pr.BLUE)


def save_state() -> dict[str, Any]:
    return {}


def restore_state(state: dict[str, Any]):
    pass

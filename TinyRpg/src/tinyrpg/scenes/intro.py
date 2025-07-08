from typing import Any, Optional

import pyray as pr

from tinyrpg.engine import FixedCamera, Scene, SceneEvent, load_texture, unload_resources
from tinyrpg.engine.base.drawing import draw_text_outlined_v

events: list[SceneEvent] = []


def next_event() -> Optional[SceneEvent]:
    return events.pop(0) if events else None


def init(previous_scene: Optional[Scene] = None):
    global texture, fixed_camera
    fixed_camera = FixedCamera()
    texture = load_texture("screen-intro")


def release():
    unload_resources()


def update(dt: float):
    if pr.is_key_pressed(pr.KeyboardKey.KEY_X):
        events.append(SceneEvent("change", ("intro", "keypress")))


def draw():
    pr.begin_mode_2d(fixed_camera.camera)
    pr.draw_texture(texture, 0, 0, pr.WHITE)

    text_width = pr.measure_text("TinyRpg", 48)
    text_pos = pr.Vector2(128 - text_width / 2, 128 - 48 / 2)
    draw_text_outlined_v("TinyRpg", text_pos, 48, pr.WHITE, pr.BLACK)

    text_width = pr.measure_text("Press [X] key to play ...", 8)
    text_pos = pr.Vector2(128 - text_width / 2, 128 + 48 / 2 + 8)
    draw_text_outlined_v("Press [X] key to play ...", text_pos, 8, pr.WHITE, pr.BLACK)

    pr.end_mode_2d()


def reset_state():
    pass


def save_state() -> dict[str, Any]:
    return {}


def restore_state(state: dict[str, Any]):
    pass

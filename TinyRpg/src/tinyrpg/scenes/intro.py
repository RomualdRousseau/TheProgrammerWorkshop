from typing import Any, Optional

import pyray as pr

from tinyrpg.constants import WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine import FixedCamera, Scene, SceneEvent, Timer, draw_text_outlined_v, load_texture, unload_resources

INTRO_FONT_SIZE = 48

timer = Timer(5)
events: list[SceneEvent] = []


def next_event() -> Optional[SceneEvent]:
    return events.pop(0) if events else None


def init(previous_scene: Optional[Scene] = None):
    global texture, fixed_camera
    fixed_camera = FixedCamera()
    texture = load_texture("screen-intro")
    timer.set()


def release():
    unload_resources()


def update(dt: float):
    timer.update(dt)

    if timer.is_elapsed() or pr.is_key_pressed(pr.KeyboardKey.KEY_X):
        events.append(SceneEvent("change", ("intro", "goto_menu")))


def draw():
    pr.begin_mode_2d(fixed_camera.camera)
    pr.draw_texture(texture, 0, 0, pr.WHITE)

    text_width = pr.measure_text("TinyRpg", INTRO_FONT_SIZE)
    text_pos = pr.Vector2((WORLD_WIDTH - text_width) / 2, (WORLD_HEIGHT - INTRO_FONT_SIZE) / 2)
    draw_text_outlined_v("TinyRpg", text_pos, INTRO_FONT_SIZE, pr.WHITE, pr.BLACK)

    pr.end_mode_2d()


def reset_state():
    pass


def save_state() -> dict[str, Any]:
    return {}


def restore_state(state: dict[str, Any]):
    pass

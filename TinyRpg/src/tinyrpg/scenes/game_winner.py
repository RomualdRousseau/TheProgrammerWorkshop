from typing import Any, Optional

import pyray as pr

from tinyrpg.constants import INPUT_GOTO_MENU, WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine import FixedCamera, Scene, SceneEvent, draw_text_outlined_v, is_action_pressed, unload_resources


class GameWinner:
    def __init__(self):
        self.events: list[SceneEvent] = []

    def next_event(self) -> Optional[SceneEvent]:
        return self.events.pop(0) if len(self.events) > 0 else None

    def init(self, previous_scene: Optional[Scene] = None):
        self.fixed_camera = FixedCamera()

        image = pr.load_image_from_screen()
        pr.image_resize(image, WORLD_WIDTH, WORLD_HEIGHT)
        self.texture = pr.load_texture_from_image(image)
        pr.unload_image(image)

    def release(self):
        unload_resources()

    def update(self, dt: float):
        if is_action_pressed(INPUT_GOTO_MENU):
            self.events.append(SceneEvent("quit", ()))

    def draw(self):
        pr.clear_background(pr.WHITE)
        pr.begin_mode_2d(self.fixed_camera.camera)
        pr.draw_texture(self.texture, 0, 0, pr.color_alpha(pr.WHITE, 0.5))
        text_width = pr.measure_text("YOU WIN", 16)
        text_pos = pr.Vector2((WORLD_WIDTH - text_width) / 2, (WORLD_HEIGHT - 16) / 2)
        draw_text_outlined_v("YOU WIN", text_pos, 16, pr.WHITE, pr.BLACK)
        pr.end_mode_2d()

    def reset_state(self):
        pass

    def save_state(self) -> dict[str, Any]:
        return {}

    def restore_state(self, state: dict[str, Any]):
        pass

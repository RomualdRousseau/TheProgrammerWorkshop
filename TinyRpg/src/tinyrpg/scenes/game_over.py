from typing import Any, Optional

import pyray as pr

from tinyrpg.constants import WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine import FixedCamera, Scene, SceneEvent, get_database, unload_resources
from tinyrpg.widgets import GameOverBox


class GameOver:
    def __init__(self, message: str, color: pr.Color):
        self.message = message
        self.color = color
        self.events: list[SceneEvent] = []

    def next_event(self) -> Optional[SceneEvent]:
        return self.events.pop(0) if len(self.events) > 0 else None

    def init(self, previous_scene: Optional[Scene] = None):
        self.fixed_camera = FixedCamera()
        self.text_box = GameOverBox(get_database().select_dict("messages")["quest_grace"][self.message][0])

        image = pr.load_image_from_screen()
        pr.image_resize(image, WORLD_WIDTH, WORLD_HEIGHT)
        self.texture = pr.load_texture_from_image(image)
        pr.unload_image(image)

    def release(self):
        unload_resources()

    def update(self, dt: float):
        self.text_box.update(dt)

        if self.text_box.closed:
            self.events.append(SceneEvent("quit", ()))

    def draw(self):
        pr.clear_background(self.color)
        pr.begin_mode_2d(self.fixed_camera.camera)
        pr.draw_texture(self.texture, 0, 0, pr.color_alpha(pr.WHITE, 0.5))
        self.text_box.draw()
        pr.end_mode_2d()

    def reset_state(self):
        pass

    def save_state(self) -> dict[str, Any]:
        return {}

    def restore_state(self, state: dict[str, Any]):
        pass

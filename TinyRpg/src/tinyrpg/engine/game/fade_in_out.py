from typing import Any, Optional

import pyray as pr

from tinyrpg.engine.game.scene import Scene, SceneEvent


class FadeInOut:
    def __init__(self, state: str, next_scene: Scene):
        self.state = state
        self.next_scene = next_scene

    def next_event(self) -> Optional[SceneEvent]:
        return self.next_scene.next_event()

    def init(self, previous_scene: Optional[Scene] = None):
        if previous_scene:
            previous_scene.draw()
            image = pr.load_image_from_screen()
            self.texture = pr.load_texture_from_image(image)
            pr.unload_image(image)
            previous_scene.release()
        else:
            self.texture = None

        self.time = 0
        self.next_scene.init(previous_scene)

    def release(self):
        self.next_scene.release()

    def update(self, dt: float):
        self.time += dt
        if self.time > 1.0:
            self.next_scene.update(dt)

    def draw(self):
        if self.next_scene:
            self.next_scene.draw()
        if self.texture and self.time <= 1.0:
            pr.draw_texture(self.texture, 0, 0, pr.color_alpha(pr.WHITE, 1.0 - min(self.time, 1.0)))

    def reset_state(self):
        self.next_scene.reset_state()

    def save_state(self) -> dict[str, Any]:
        return self.next_scene.save_state()

    def restore_state(self, state: dict[str, Any]):
        self.next_scene.restore_state(state)

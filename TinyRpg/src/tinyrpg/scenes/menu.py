from typing import Any, Optional

import pyray as pr

from tinyrpg.engine import FixedCamera, Scene, SceneEvent, unload_resources
from tinyrpg.widgets import MenuBox
from tinyrpg.widgets.menu_box import MenuItem


class Menu:
    def __init__(self):
        self.first_use = True
        self.events: list[SceneEvent] = []

    def next_event(self) -> Optional[SceneEvent]:
        return self.events.pop(0) if len(self.events) > 0 else None

    def init(self, previous_scene: Optional[Scene] = None):
        self.menu_box = MenuBox(not self.first_use)
        self.fixed_camera = FixedCamera()
        self.first_use = False

    def release(self):
        unload_resources()

    def update(self, dt: float):
        self.menu_box.update(dt)

        match self.menu_box.selected_item:
            case MenuItem.LOAD:
                self.events.append(SceneEvent("load", ()))
                self.events.append(SceneEvent("restore", ()))
            case MenuItem.CONTINUE:
                self.events.append(SceneEvent("restore", ()))
            case MenuItem.SAVE:
                self.events.append(SceneEvent("save", ()))
                self.events.append(SceneEvent("restore", ()))
            case MenuItem.NEW:
                self.events.append(SceneEvent("reset", ()))
                self.events.append(SceneEvent("change", ("menu", "goto_level")))
            case MenuItem.QUIT:
                self.events.append(SceneEvent("quit", ()))

    def draw(self):
        pr.clear_background(pr.RED)
        pr.begin_mode_2d(self.fixed_camera.camera)
        self.menu_box.draw()
        pr.end_mode_2d()

    def reset_state(self):
        pass

    def save_state(self) -> dict[str, Any]:
        return {}

    def restore_state(self, state: dict[str, Any]):
        pass

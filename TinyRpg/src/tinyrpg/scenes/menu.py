from typing import Any, Optional

import pyray as pr

from tinyrpg.constants import WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine import FixedCamera, Scene, SceneEvent, unload_resources
from tinyrpg.engine.base.resources import load_texture
from tinyrpg.widgets import MenuBox, MenuItem


class Menu:
    def __init__(self):
        self.first_use = True
        self.events: list[SceneEvent] = []

    def next_event(self) -> Optional[SceneEvent]:
        return self.events.pop(0) if len(self.events) > 0 else None

    def init(self, previous_scene: Optional[Scene] = None):
        self.menu_box = MenuBox(not self.first_use)
        self.fixed_camera = FixedCamera()

        if self.first_use:
            self.texture = load_texture("screen-menu")
        else:
            image = pr.load_image_from_screen()
            pr.image_resize(image, WORLD_WIDTH, WORLD_HEIGHT)
            self.texture = pr.load_texture_from_image(image)
            pr.unload_image(image)

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
                self.events.append(SceneEvent("change", ("menu", "goto_level1")))
            case MenuItem.QUIT:
                self.events.append(SceneEvent("quit", ()))

    def draw(self):
        pr.clear_background(pr.WHITE)
        pr.begin_mode_2d(self.fixed_camera.camera)
        pr.draw_texture(self.texture, 0, 0, pr.color_alpha(pr.WHITE, 0.5))
        self.menu_box.draw()
        pr.end_mode_2d()

    def reset_state(self):
        pass

    def save_state(self) -> dict[str, Any]:
        return {}

    def restore_state(self, state: dict[str, Any]):
        pass

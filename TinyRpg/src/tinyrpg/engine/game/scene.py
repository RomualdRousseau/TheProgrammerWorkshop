from __future__ import annotations

from typing import Protocol


class Scene(Protocol):
    def init(self): ...

    def release(self): ...

    def update(self, dt: float): ...

    def draw(self): ...

    def get_state_and_input(self) -> tuple[str, str]: ...


def change_scene(scene: Scene, state_transition: dict[str, dict[str, Scene]]) -> Scene:
    state, input = scene.get_state_and_input()
    new_scene = state_transition[state].get(input)
    if new_scene:
        new_scene.init()
    return new_scene or scene

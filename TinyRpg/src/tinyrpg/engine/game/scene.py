from __future__ import annotations

from typing import Any, Optional, Protocol


class Saveable(Protocol):
    def save_state(self) -> dict[str, Any]: ...

    def restore_state(self, state: dict[str, Any]): ...


class Scene(Protocol):
    def init(self, previous_scene: Optional[Scene] = None): ...

    def release(self): ...

    def update(self, dt: float): ...

    def draw(self): ...

    def get_state_and_input(self) -> tuple[str, str]: ...

    def save_state(self) -> dict[str, Any]: ...

    def restore_state(self, state: dict[str, Any]): ...


def change_scene(scene: Scene, state_transition: dict[str, dict[str, Scene]]) -> Scene:
    state, input = scene.get_state_and_input()
    new_scene = state_transition[state].get(input)
    if new_scene:
        new_scene.init(scene)
    return new_scene or scene

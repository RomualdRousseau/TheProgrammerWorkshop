from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Protocol


@dataclass
class SceneEvent:
    name: str
    args: tuple[str, ...]


class Saveable(Protocol):
    def save_state(self) -> dict[str, Any]: ...

    def restore_state(self, state: dict[str, Any]): ...


class Scene(Protocol):
    def next_event(self) -> Optional[SceneEvent]: ...

    def init(self, previous_scene: Optional[Scene] = None): ...

    def release(self): ...

    def update(self, dt: float): ...

    def draw(self): ...

    def save_state(self) -> dict[str, Any]: ...

    def restore_state(self, state: dict[str, Any]): ...


def change_scene(scene: Scene, state: str, input: str, state_transition: dict[str, dict[str, Scene]]) -> Scene:
    new_scene = state_transition[state].get(input)
    if new_scene:
        new_scene.init(scene)
    return new_scene or scene

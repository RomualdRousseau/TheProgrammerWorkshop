from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional, Protocol

from tinyrpg.engine.game.inventory import get_player_inventory
from tinyrpg.engine.utils.pickle import PRPickler, PRUnpickler


@dataclass
class SceneEvent:
    name: str
    args: tuple[str, ...]


class Scene(Protocol):
    def next_event(self) -> Optional[SceneEvent]: ...

    def init(self, previous_scene: Optional[Scene] = None): ...

    def release(self): ...

    def update(self, dt: float): ...

    def draw(self): ...

    def reset_state(self): ...

    def save_state(self) -> dict[str, Any]: ...

    def restore_state(self, state: dict[str, Any]): ...


SceneState = tuple[str, Scene]

_state_stack: list[SceneState] = []


def push_state(state: SceneState):
    _state_stack.append(state)


def pop_state() -> Optional[SceneState]:
    return _state_stack.pop() if _state_stack else None


def peek_state() -> Optional[SceneState]:
    return _state_stack[-1] if _state_stack else None


def reset_states(states: dict[str, Scene]):
    get_player_inventory().reset_state()
    for scene in states.values():
        scene.reset_state()


def save_states(file_path: str, states: dict[str, Scene]):
    game_state = {
        "inventory": get_player_inventory().save_state(),
        **{key: scene.save_state() for key, scene in states.items()},
    }

    if current_state := peek_state():
        game_state["initial"] = {"state": current_state[0]}

    with open(file_path, "wb") as fp:
        PRPickler(fp).dump(game_state)


def load_states(file_path: str, states: dict[str, Scene]):
    if not os.path.exists(file_path):
        return

    with open(file_path, "rb") as fp:
        game_state = PRUnpickler(fp).load()

    get_player_inventory().restore_state(game_state["inventory"])

    for key, scene in states.items():
        scene.restore_state(game_state[key])

    initial = game_state.get("initial")
    if initial:
        push_state((initial["state"], states[initial["state"]]))


def change_scene(
    scene: Scene,
    state_key: str,
    state_input: str,
    transition_table: dict[str, dict[str, Scene]],
) -> Scene:
    if new_scene := transition_table[state_key].get(state_input):
        new_scene.init(scene)
        return new_scene
    return scene


def restore_scene(scene: Scene) -> Scene:
    state = pop_state()
    if state:
        _, new_scene = state
        if new_scene:
            new_scene.init(scene)
            return new_scene
    return scene


def process_scene_event(
    event: SceneEvent,
    scene: Scene,
    states: dict[str, Scene],
    transition_table: dict[str, dict[str, Scene]],
) -> tuple[Scene, bool]:
    should_close = False
    match event:
        case SceneEvent("change", (state, input)):
            scene = change_scene(scene, state, input, transition_table)
        case SceneEvent("restore", ()):
            scene = restore_scene(scene)
        case SceneEvent("reset", ()):
            reset_states(states)
        case SceneEvent("save", ()):
            save_states("saved/state.pkl", states)
        case SceneEvent("load", ()):
            load_states("saved/state.pkl", states)
        case SceneEvent("quit", ()):
            should_close = True
    return scene, should_close

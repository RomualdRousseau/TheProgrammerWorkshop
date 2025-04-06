from typing import Protocol

from spacerace import ACTION_KEYPRESS, ACTION_NONE, ACTION_TIMEOUT
from spacerace.scenes import game, game_over, intro


class Scene(Protocol):
    def init(self): ...

    def release(self): ...

    def update(self, dt: float): ...

    def draw(self): ...

    def get_action(self) -> str: ...


INITIAL_SCENE: Scene = intro

SCENES: list[Scene] = [intro, game, game_over]

ACTIONS: list[str] = [ACTION_KEYPRESS, ACTION_TIMEOUT, ACTION_NONE]

TRANSITION_TABLE: dict[tuple[Scene, str], Scene] = {
    (SCENES[0], ACTIONS[0]): SCENES[1],
    (SCENES[1], ACTIONS[1]): SCENES[2],
    (SCENES[2], ACTIONS[0]): SCENES[0],
    (SCENES[2], ACTIONS[1]): SCENES[0],
}


def get_next_scene(scene: Scene, transition_table: dict[tuple[Scene, str], Scene] = TRANSITION_TABLE) -> Scene:
    next_scene = transition_table.get((scene, scene.get_action()), scene)
    if scene != next_scene:
        scene.release()
        next_scene.init()
    return next_scene

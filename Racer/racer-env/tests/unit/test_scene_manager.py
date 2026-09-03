from typing import Any

from racer_env.core.input import Action, InputHandler
from racer_env.core.scene_manager import Scene, SceneManager


class MockInput:
    def get_action(self) -> Action:
        return Action.IDLE


class MockScene:
    """Mock implementation of the Scene protocol for testing."""

    def __init__(self, next_scene: Scene | None = None):
        self.updated = False
        self.drawn = False
        self.last_state = None
        self.next_scene_to_return = next_scene

    def update(self, dt: float, state: Any, inputs: InputHandler) -> tuple[Any, Scene | None]:
        self.updated = True
        self.last_state = state
        return f"updated_{state}", self.next_scene_to_return

    def draw(self, state: Any) -> None:
        self.drawn = True
        self.last_state = state


def test_scene_manager_transition():
    """Verify that SceneManager transitions to the requested scene."""
    manager = SceneManager()
    scene_b = MockScene()
    scene_a = MockScene(next_scene=scene_b)
    inputs = MockInput()
    initial_state = "initial"

    # Manual transition
    manager.transition_to(scene_a)
    assert manager.current_scene is None

    # Update triggers transition to scene_a, then scene_a update returns scene_b
    next_state = manager.update(0.016, initial_state, inputs)
    assert manager.current_scene == scene_b
    assert scene_a.updated
    assert scene_a.last_state == initial_state
    assert next_state == "updated_initial"


def test_scene_manager_draw():
    """Verify that SceneManager draws the active scene."""
    manager = SceneManager()
    scene = MockScene()
    inputs = MockInput()
    state = "some_state"

    manager.transition_to(scene)
    next_state = manager.update(0.016, state, inputs)
    manager.draw(next_state)
    assert scene.drawn
    assert scene.last_state == next_state


def test_scene_manager_no_scene():
    """Verify that SceneManager handles update and draw with no scene."""
    manager = SceneManager()
    inputs = MockInput()
    state = "some_state"

    # Update with no scene should return the state unchanged
    next_state = manager.update(0.016, state, inputs)
    assert next_state == state

    # Draw with no scene should not raise any errors
    manager.draw(state)

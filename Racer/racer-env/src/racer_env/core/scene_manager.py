from typing import Any, Protocol

from racer_env.core.input import InputHandler


class Scene(Protocol):
    """Protocol interface for all game scenes."""

    def update(self, dt: float, state: Any, inputs: InputHandler) -> tuple[Any, "Scene | None"]:
        """Update scene logic and return the next state and next scene."""
        ...

    def draw(self, state: Any) -> None:
        """Render the scene using the provided state."""
        ...


class SceneManager:
    """Manages scene transitions and current active scene."""

    def __init__(self):
        self._current_scene: Scene | None = None
        self._next_scene: Scene | None = None

    @property
    def current_scene(self) -> Scene | None:
        return self._current_scene

    def transition_to(self, scene: Scene):
        """Request a transition to a new scene."""
        self._next_scene = scene

    def update(self, dt: float, state: Any, inputs: InputHandler) -> Any:
        """Update current scene, handle transitions, and return next state."""
        if self._next_scene:
            self._current_scene = self._next_scene
            self._next_scene = None

        if self._current_scene:
            next_state, next_scene = self._current_scene.update(dt, state, inputs)
            if next_scene:
                self._current_scene = next_scene
            return next_state
        return state

    def draw(self, state: Any):
        """Draw current active scene with the provided state."""
        if self._current_scene:
            self._current_scene.draw(state)

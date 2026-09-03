from typing import Any

from racer_env.core.input import Action, InputHandler
from racer_env.core.scene_manager import Scene
from racer_env.game.gameplay import init_gameplay_state, update_gameplay
from racer_env.game.state import GameState
from racer_env.ui.renderer import (
    draw_game_over_scene,
    draw_game_scene,
    draw_start_scene,
)


class StartScene:
    """Initial scene showing the start screen."""

    def update(
        self, dt: float, state: GameState, inputs: InputHandler
    ) -> tuple[GameState, "Scene | None"]:
        action = inputs.get_action()
        if action == Action.START:
            return init_gameplay_state(), GameScene()
        return state, None

    def draw(self, state: Any) -> None:
        """Draw the start screen."""
        draw_start_scene()


class GameScene:
    """Core gameplay scene handling simulation and physics."""

    def update(
        self, dt: float, state: GameState, inputs: InputHandler
    ) -> tuple[GameState, "Scene | None"]:
        if state.game_over or state.won:
            return state, GameOverScene()

        next_state = update_gameplay(dt, state, inputs)

        if next_state.game_over or next_state.won:
            return next_state, GameOverScene()

        return next_state, None

    def draw(self, state: GameState) -> None:
        """Render the game world."""
        draw_game_scene(state)


class SimulationScene:
    """Scene for agents and testing, only runs gameplay simulation."""

    def update(
        self, dt: float, state: GameState, inputs: InputHandler
    ) -> tuple[GameState, "Scene | None"]:
        # No transitions in simulation mode
        return update_gameplay(dt, state, inputs), None

    def draw(self, state: GameState) -> None:
        """Simulation scene might still be drawn if render_mode is human."""
        draw_game_scene(state)


class GameOverScene:
    """Scene shown when the game ends (Win or Loss)."""

    def update(
        self, dt: float, state: GameState, inputs: InputHandler
    ) -> tuple[GameState, "Scene | None"]:
        action = inputs.get_action()
        if action == Action.START:
            return init_gameplay_state(), GameScene()
        return state, None

    def draw(self, state: GameState) -> None:
        """Render the game over screen."""
        draw_game_over_scene(state)

from unittest.mock import MagicMock

from racer_env.core.input import Action
from racer_env.game.gameplay import init_gameplay_state
from racer_env.game.scenes import (
    GameOverScene,
    GameScene,
    SimulationScene,
    StartScene,
)


def test_start_scene_transition():
    """Verify StartScene transitions to GameScene on Action.START."""
    scene = StartScene()
    state = init_gameplay_state()
    mock_input = MagicMock()

    # No start action
    mock_input.get_action.return_value = Action.IDLE
    next_state, next_scene = scene.update(0.016, state, mock_input)
    assert next_scene is None
    assert next_state == state

    # Start action
    mock_input.get_action.return_value = Action.START
    next_state, next_scene = scene.update(0.016, state, mock_input)
    assert isinstance(next_scene, GameScene)


def test_game_scene_logic():
    """Verify GameScene update delegates to gameplay and handles transitions."""
    scene = GameScene()
    state = init_gameplay_state()
    mock_input = MagicMock()
    mock_input.get_action.return_value = Action.IDLE

    # Normal update
    next_state, next_scene = scene.update(0.016, state, mock_input)
    assert next_scene is None
    assert next_state.timer > 0

    # Game over transition
    state.game_over = True
    next_state, next_scene = scene.update(0.016, state, mock_input)
    assert isinstance(next_scene, GameOverScene)


def test_simulation_scene_no_transition():
    """Verify SimulationScene never transitions."""
    scene = SimulationScene()
    state = init_gameplay_state()
    mock_input = MagicMock()
    mock_input.get_action.return_value = Action.IDLE

    state.game_over = True
    next_state, next_scene = scene.update(0.016, state, mock_input)
    assert next_scene is None


def test_game_over_scene_restart():
    """Verify GameOverScene transitions to GameScene on Action.START."""
    scene = GameOverScene()
    state = init_gameplay_state()
    mock_input = MagicMock()

    mock_input.get_action.return_value = Action.START
    next_state, next_scene = scene.update(0.016, state, mock_input)
    assert isinstance(next_scene, GameScene)

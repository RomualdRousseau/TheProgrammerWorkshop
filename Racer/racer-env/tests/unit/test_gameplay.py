from unittest.mock import MagicMock, patch

import pyray as pr
from racer_env.core.config import Config
from racer_env.core.input import Action
from racer_env.game.gameplay import init_gameplay_state, update_gameplay
from racer_env.game.state import Entity, GameState


def test_init_gameplay_state():
    """Verify that gameplay state is correctly initialized."""
    state = init_gameplay_state()
    assert isinstance(state, GameState)
    assert state.player.width == 64
    assert state.player.height == 64
    assert len(state.obstacles) == 0
    assert state.score == 0
    assert not state.game_over
    assert not state.won


def test_update_gameplay_movement():
    """Verify player movement in update_gameplay."""
    state = init_gameplay_state()
    initial_x = state.player.position.x
    mock_input = MagicMock()

    # Move Left
    mock_input.get_action.return_value = Action.LEFT
    state = update_gameplay(0.1, state, mock_input)
    assert state.player.position.x < initial_x

    # Move Right
    mock_input.get_action.return_value = Action.RIGHT
    state = update_gameplay(0.1, state, mock_input)
    assert state.player.position.x == initial_x


def test_update_gameplay_collision():
    """Verify collision detection in update_gameplay."""
    state = init_gameplay_state()
    # Place obstacle on top of player
    state.obstacles.append(
        Entity(
            position=pr.Vector2(state.player.position.x, state.player.position.y),
            velocity=pr.Vector2(0, 0),
            width=64,
            height=64,
        )
    )
    mock_input = MagicMock()
    mock_input.get_action.return_value = Action.IDLE

    with patch("pyray.check_collision_recs", return_value=True):
        state = update_gameplay(0.016, state, mock_input)
        assert state.game_over


def test_update_gameplay_win_timer():
    """Verify win condition when timer exceeds limit."""
    state = init_gameplay_state()
    state.timer = Config.GAME_TIMER - 0.01
    mock_input = MagicMock()
    mock_input.get_action.return_value = Action.IDLE

    state = update_gameplay(0.02, state, mock_input)
    assert state.won

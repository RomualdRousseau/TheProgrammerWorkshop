from unittest.mock import patch

import pyray as pr
from racer_env.core.input import Action, AgentInput, KeyboardInput, RandomInput


def test_agent_input():
    """Verify that AgentInput correctly stores and returns the set action."""
    handler = AgentInput()
    assert handler.get_action() == Action.IDLE

    handler.set_action(Action.LEFT)
    assert handler.get_action() == Action.LEFT

    handler.set_action(Action.RIGHT)
    assert handler.get_action() == Action.RIGHT


def test_random_input():
    """Verify that RandomInput returns valid actions."""
    handler = RandomInput()
    for _ in range(10):
        action = handler.get_action()
        assert action in Action


def test_keyboard_input():
    """Verify that KeyboardInput correctly maps Raylib keys to Actions."""
    handler = KeyboardInput()

    with patch("pyray.is_key_down") as mock_key_down:
        # Test Left
        mock_key_down.side_effect = lambda key: key == pr.KeyboardKey.KEY_LEFT
        assert handler.get_action() == Action.LEFT

        # Test Right
        mock_key_down.side_effect = lambda key: key == pr.KeyboardKey.KEY_RIGHT
        assert handler.get_action() == Action.RIGHT

        # Test Idle (No keys)
        mock_key_down.side_effect = lambda key: False
        assert handler.get_action() == Action.IDLE

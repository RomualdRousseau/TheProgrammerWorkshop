from enum import IntEnum
from typing import Protocol

import pyray as pr


class Action(IntEnum):
    IDLE = 0
    LEFT = 1
    RIGHT = 2
    START = 3


class InputHandler(Protocol):
    """Protocol interface for receiving player input."""

    def get_action(self) -> Action: ...


class KeyboardInput:
    """Handles standard keyboard input via Raylib."""

    def get_action(self) -> Action:
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
            return Action.LEFT
        if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
            return Action.RIGHT
        if pr.is_key_down(pr.KeyboardKey.KEY_SPACE):
            return Action.START
        return Action.IDLE


class AgentInput:
    """Handles input from an RL agent."""

    def __init__(self):
        self._action: Action = Action.IDLE

    def set_action(self, action: Action):
        self._action = action

    def get_action(self) -> Action:
        return self._action


class RandomInput:
    """Generates random actions for testing purposes."""

    def get_action(self) -> Action:
        import random

        return Action(random.choice([Action.IDLE, Action.LEFT, Action.RIGHT]))

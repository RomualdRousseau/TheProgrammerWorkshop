"""Keyboard input: the human InputSource backed by raylib key polling.

Player 1 uses W/S, player 2 uses the arrow keys, Space confirms.
"""

import pyray as pr

from spacerace.core.input import InputCommand


def poll(_dt: float) -> InputCommand:
    """Sample the keyboard for this frame's command."""
    return InputCommand(
        p1_up=pr.is_key_down(pr.KeyboardKey.KEY_W),
        p1_down=pr.is_key_down(pr.KeyboardKey.KEY_S),
        p2_up=pr.is_key_down(pr.KeyboardKey.KEY_UP),
        p2_down=pr.is_key_down(pr.KeyboardKey.KEY_DOWN),
        confirm=pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE),
    )

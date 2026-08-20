"""Pure state-transition functions: the physics of the Space Race world."""

from dataclasses import replace

from spacerace.core import constant
from spacerace.core.math import clamp
from spacerace.core.state import Player


def move_player(player: Player, velocity_y: float, dt: float) -> Player:
    """Move a rocket vertically, clamped so it never leaves the field."""
    max_y = float(constant.SCREEN_SIZE - constant.PLAYER_HEIGHT)
    y = clamp(player.y + velocity_y * dt, 0.0, max_y)
    return replace(player, y=y)

"""Pure audio helpers: altitude-to-progress mapping for ship engine beeps."""

from spacerace.core import constant
from spacerace.core.math import clamp


def ship_altitude_progress(y: float) -> float:
    """Map a rocket's top-left y coordinate to an ascent progress in [0.0, 1.0].

    0.0 is the ship centered at the start row, 1.0 is the ship centered at the
    goal row. The screen y axis points down, so lower y means higher altitude.
    """
    half_height = constant.PLAYER_HEIGHT / 2.0
    bottom = constant.START_Y + half_height
    top = constant.GOAL_ROW + half_height
    return clamp((bottom - y) / (bottom - top), 0.0, 1.0)

"""Gameplay logic module operating strictly on core abstractions."""

from greensquare.core.constant import WINDOW_HEIGHT, WINDOW_WIDTH, PLAYER_SIZE
from greensquare.core.physics import update_player_physics
from greensquare.core.state import InputState, PlayerState


def init_player() -> PlayerState:
    """Initialize player at screen center."""
    start_x = (WINDOW_WIDTH - PLAYER_SIZE) / 2.0
    start_y = (WINDOW_HEIGHT - PLAYER_SIZE) / 2.0
    return PlayerState(x=start_x, y=start_y)


def update_game(player: PlayerState, input_state: InputState, dt: float) -> PlayerState:
    """Update gameplay state for one frame step."""
    return update_player_physics(player, input_state, dt)

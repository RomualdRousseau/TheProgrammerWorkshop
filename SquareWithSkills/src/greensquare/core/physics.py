"""Pure physics functions, smooth acceleration/friction easing, and boundary calculations."""

import math
from greensquare.core.constant import (
    FRICTION_DECAY,
    MAX_TRAIL_LENGTH,
    MAX_X,
    MAX_Y,
    MIN_X,
    MIN_Y,
    PLAYER_SPEED,
)
from greensquare.core.state import InputState, PlayerState


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min_val and max_val."""
    return max(min_val, min(value, max_val))


def update_player_physics(
    player: PlayerState, input_state: InputState, dt: float
) -> PlayerState:
    """Update player velocity easing, position, trail, and boundary clamping."""
    target_vx = input_state.move_x * PLAYER_SPEED
    target_vy = input_state.move_y * PLAYER_SPEED

    # Smooth exponential decay easing towards target velocity
    blend = 1.0 - math.exp(-FRICTION_DECAY * dt)
    new_vx = player.vx + (target_vx - player.vx) * blend
    new_vy = player.vy + (target_vy - player.vy) * blend

    # Zero out near-zero velocities for stability
    if abs(new_vx) < 0.1:
        new_vx = 0.0
    if abs(new_vy) < 0.1:
        new_vy = 0.0

    new_x = clamp(player.x + new_vx * dt, MIN_X, MAX_X)
    new_y = clamp(player.y + new_vy * dt, MIN_Y, MAX_Y)

    # Maintain trail history when position or velocity is active
    new_trail = player.trail
    if (new_x, new_y) != (player.x, player.y) or abs(new_vx) > 1.0 or abs(new_vy) > 1.0:
        new_trail = ((player.x, player.y),) + player.trail[: MAX_TRAIL_LENGTH - 1]

    return PlayerState(x=new_x, y=new_y, vx=new_vx, vy=new_vy, trail=new_trail)

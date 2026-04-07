"""
Orchestration of game logic and state updates.
"""

import random
import pyray as pr
from permanence_env.game.state import (
    Ball,
    GameState,
    TargetRect,
)
from permanence_env.core.physics import (
    apply_physics,
    get_friction_force,
    get_toward_force,
    handle_boundary_collisions,
)
from permanence_env.utils.constant import (
    GRID_CELL_SIZE,
    GRID_SIZE,
    TARGET_RECT_SIZE,
)
from permanence_env.utils.helper import get_random_target_pos


def init_game() -> GameState:
    """
    Initialize a new game state with randomized parameters.

    Returns:
        GameState: The newly created game state.
    """
    # Grid pixel dimensions (the playable area)
    grid_px_size = GRID_SIZE * GRID_CELL_SIZE
    ball_radius = GRID_CELL_SIZE / 2.0

    # Random position for ball inside the grid, accounting for radius
    ball_pos = pr.Vector2(
        random.uniform(ball_radius, grid_px_size - ball_radius),
        random.uniform(ball_radius, grid_px_size - ball_radius),
    )

    # Random position for target rect inside the grid, with 2-cell border
    # GRID_SIZE is 20, TARGET_RECT_SIZE is 3. 
    # Border 2 cells: min index 2, max index (20 - 3 - 2) = 15.
    rect_grid_x = random.randint(2, GRID_SIZE - TARGET_RECT_SIZE - 2)
    rect_grid_y = random.randint(2, GRID_SIZE - TARGET_RECT_SIZE - 2)

    # Random target point inside rect
    target_pos = get_random_target_pos(rect_grid_x, rect_grid_y)

    target = TargetRect(rect_grid_x, rect_grid_y, target_pos)

    # Random mass and friction
    ball = Ball(
        pos=ball_pos,
        velocity=pr.Vector2(0, 0),
        mass=random.uniform(1.0, 5.0),
        friction=random.uniform(0.1, 0.5),
        radius=ball_radius,
    )
    return GameState(ball, target)


def update_game(state: GameState, dt: float, initial_speed: float) -> GameState:
    """
    Update the entire game simulation for a single frame.

    Args:
        state (GameState): The game state to update.
        dt (float): Delta time since last update.
        initial_speed (float): The speed at which the ball moves toward the target.

    Returns:
        GameState: The updated game state.
    """
    # Toggle layer 2 visibility
    if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
        state.show_layer2 = not state.show_layer2

    # Sum forces
    friction = get_friction_force(state.ball)
    toward = get_toward_force(state.ball, state.target.wp1_pos, initial_speed)
    net_force = pr.vector2_add(friction, toward)

    # Physics: Update ball state
    apply_physics(state.ball, net_force, dt)

    # Rebound on boundaries
    handle_boundary_collisions(state.ball, float(GRID_SIZE * GRID_CELL_SIZE))

    # Update ball animation
    state.ball.animation_timer += dt
    if state.ball.animation_timer >= 1.0 / 3.0:  # 3 FPS
        state.ball.animation_frame = (state.ball.animation_frame + 1) % 3
        state.ball.animation_timer = 0.0

    return state

"""
Physics integration and movement logic.
"""

import pyray as pr

from permanence_env.game.state import Ball
from permanence_env.utils.constant import EPSILON


def apply_physics(ball: Ball, force_sum: pr.Vector2, dt: float) -> None:
    """
    Apply Euler integration to the ball's position and velocity using the net force.
    """
    # a = F/m
    accel = pr.vector2_scale(force_sum, 1.0 / ball.mass)

    # v = v + a*dt
    ball.velocity = pr.vector2_add(ball.velocity, pr.vector2_scale(accel, dt))

    # p = p + v*dt
    ball.pos = pr.vector2_add(ball.pos, pr.vector2_scale(ball.velocity, dt))


def handle_boundary_collisions(ball: Ball, grid_px_size: float) -> None:
    """
    Check for grid boundary collisions and bounce the ball if necessary.
    Inverts velocity and clamps position to the boundary, accounting for radius.
    """
    # X Boundary
    if ball.pos.x <= ball.radius:
        ball.pos.x = ball.radius
        ball.velocity.x *= -1
    elif ball.pos.x >= grid_px_size - ball.radius:
        ball.pos.x = grid_px_size - ball.radius
        ball.velocity.x *= -1

    # Y Boundary
    if ball.pos.y <= ball.radius:
        ball.pos.y = ball.radius
        ball.velocity.y *= -1
    elif ball.pos.y >= grid_px_size - ball.radius:
        ball.pos.y = grid_px_size - ball.radius
        ball.velocity.y *= -1


def get_friction_force(ball: Ball) -> pr.Vector2:
    """Calculate friction force opposing velocity."""
    return pr.vector2_scale(ball.velocity, -ball.friction)


def get_toward_force(ball: Ball, target: pr.Vector2, speed: float) -> pr.Vector2:
    """Calculate acceleration force towards target."""
    direction = pr.vector2_subtract(target, ball.pos)
    dist = pr.vector2_length(direction)

    # Normalize direction, add EPSILON to avoid division by zero
    normalized_dir = pr.vector2_scale(direction, 1.0 / (dist + EPSILON))

    # Force = direction * speed * mass
    force_magnitude = speed * ball.mass
    return pr.vector2_scale(normalized_dir, force_magnitude)

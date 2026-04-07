import pyray as pr
import pytest

from permanence_env.core.physics import (
    apply_physics,
    get_friction_force,
    get_toward_force,
    handle_boundary_collisions,
)
from permanence_env.game.state import Ball


def test_apply_physics_integration():
    """Verify Euler integration using a constant force."""
    ball = Ball(pos=pr.Vector2(0, 0), velocity=pr.Vector2(0, 0), mass=1.0, friction=0.0)
    # Apply a force F = (10, 0)
    # a = F/m = (10/1, 0) = (10, 0)
    # dt = 0.1
    # v = 0 + a*dt = (1, 0)
    # p = 0 + v*dt = (0.1, 0)
    force = pr.Vector2(10.0, 0.0)
    apply_physics(ball, force, 0.1)

    assert ball.velocity.x == pytest.approx(1.0)
    assert ball.pos.x == pytest.approx(0.1)


def test_force_calculations():
    """Verify force vector calculations."""
    ball = Ball(
        pos=pr.Vector2(0, 0), velocity=pr.Vector2(10, 0), mass=1.0, friction=0.5
    )
    target = pr.Vector2(100, 0)

    friction = get_friction_force(ball)
    accel = get_toward_force(ball, target, 50.0)

    assert friction.x < 0
    assert accel.x > 0


def test_handle_boundary_collisions():
    """Verify ball rebounds on boundaries accounting for radius."""
    grid_size = 100.0
    radius = 5.0

    # Left bound
    ball = Ball(
        pos=pr.Vector2(4, 50),
        velocity=pr.Vector2(-10, 0),
        mass=1.0,
        friction=0.0,
        radius=radius,
    )
    handle_boundary_collisions(ball, grid_size)
    assert ball.pos.x == radius
    assert ball.velocity.x == 10

    # Right bound
    ball = Ball(
        pos=pr.Vector2(96, 50),
        velocity=pr.Vector2(10, 0),
        mass=1.0,
        friction=0.0,
        radius=radius,
    )
    handle_boundary_collisions(ball, grid_size)
    assert ball.pos.x == grid_size - radius
    assert ball.velocity.x == -10

    # Top bound
    ball = Ball(
        pos=pr.Vector2(50, 4),
        velocity=pr.Vector2(0, -10),
        mass=1.0,
        friction=0.0,
        radius=radius,
    )
    handle_boundary_collisions(ball, grid_size)
    assert ball.pos.y == radius
    assert ball.velocity.y == 10

    # Bottom bound
    ball = Ball(
        pos=pr.Vector2(50, 96),
        velocity=pr.Vector2(0, 10),
        mass=1.0,
        friction=0.0,
        radius=radius,
    )
    handle_boundary_collisions(ball, grid_size)
    assert ball.pos.y == grid_size - radius
    assert ball.velocity.y == -10

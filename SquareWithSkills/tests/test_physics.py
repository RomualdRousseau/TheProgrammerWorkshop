"""Unit tests for core physics, velocity easing, motion trail, and boundary clamping."""

from greensquare.core.constant import MAX_X, MAX_Y, MIN_X, MIN_Y
from greensquare.core.physics import clamp
from greensquare.core.state import InputState, PlayerState
from greensquare.game.gameplay import init_player, update_game


def test_clamp_function() -> None:
    assert clamp(5.0, 0.0, 10.0) == 5.0
    assert clamp(-5.0, 0.0, 10.0) == 0.0
    assert clamp(15.0, 0.0, 10.0) == 10.0


def test_init_player_centered() -> None:
    player = init_player()
    assert player.x == 240.0
    assert player.y == 240.0
    assert player.vx == 0.0
    assert player.vy == 0.0
    assert player.trail == ()


def test_movement_acceleration_and_trail() -> None:
    player = PlayerState(x=100.0, y=100.0)
    input_state = InputState(move_x=1.0, move_y=0.0)
    dt = 0.1

    updated = update_game(player, input_state, dt)
    assert updated.x > 100.0
    assert updated.vx > 0.0
    assert len(updated.trail) == 1
    assert updated.trail[0] == (100.0, 100.0)


def test_deceleration_friction() -> None:
    # Moving right with high velocity, then release keys
    player = PlayerState(x=100.0, y=100.0, vx=200.0, vy=0.0)
    input_state = InputState(move_x=0.0, move_y=0.0)
    dt = 0.1

    updated = update_game(player, input_state, dt)
    assert updated.vx < 200.0  # Decelerated due to friction
    assert updated.x > 100.0


def test_boundary_clamping_left_top() -> None:
    player = PlayerState(x=10.0, y=10.0, vx=-300.0, vy=-300.0)
    input_state = InputState(move_x=-1.0, move_y=-1.0)
    dt = 1.0

    updated = update_game(player, input_state, dt)
    assert updated.x == MIN_X
    assert updated.y == MIN_Y


def test_boundary_clamping_right_bottom() -> None:
    player = PlayerState(x=470.0, y=470.0, vx=300.0, vy=300.0)
    input_state = InputState(move_x=1.0, move_y=1.0)
    dt = 1.0

    updated = update_game(player, input_state, dt)
    assert updated.x == MAX_X
    assert updated.y == MAX_Y

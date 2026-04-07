import pyray as pr
import pytest
from unittest.mock import patch
from permanence_env.game.state import Ball, GameState, TargetRect
from permanence_env.game.gameplay import update_game

def test_update_game_physics():
    """Verify update_game coordinates physics and acceleration."""
    state = GameState(
        ball=Ball(
            pos=pr.Vector2(0, 0),
            velocity=pr.Vector2(0, 0),
            mass=1.0,
            friction=0.0
        ),
        target=TargetRect(0, 0, pr.Vector2(100, 0))
    )
    
    # Run update_game
    # Direction is (1, 0), speed 50, dt 0.1 -> Accel (5, 0)
    # New velocity (5, 0) -> New pos (0.5, 0)
    state = update_game(state, 0.1, 50.0)
    
    assert state.ball.velocity.x > 0
    assert state.ball.pos.x > 0

def test_update_game_toggle_layer():
    """Verify update_game toggles layer 2 when SPACE is pressed."""
    state = GameState(
        ball=Ball(pr.Vector2(0, 0), pr.Vector2(0, 0), 1.0, 0.0),
        target=TargetRect(0, 0, pr.Vector2(0, 0)),
        show_layer2=True
    )
    
    # Mock pr.is_key_pressed to return True for SPACE
    with patch("pyray.is_key_pressed", return_value=True):
        state = update_game(state, 0.1, 0.0)
        assert state.show_layer2 is False
        
        # Press again
        state = update_game(state, 0.1, 0.0)
        assert state.show_layer2 is True

def test_update_game_animation():
    """Verify ball animation frames increment correctly."""
    state = GameState(
        ball=Ball(pr.Vector2(0, 0), pr.Vector2(0, 0), 1.0, 0.0, animation_frame=0, animation_timer=0.0),
        target=TargetRect(0, 0, pr.Vector2(0, 0))
    )
    
    # dt = 0.4 > 1/3 (0.333...)
    state = update_game(state, 0.4, 0.0)
    assert state.ball.animation_frame == 1
    assert state.ball.animation_timer == 0.0
    
    # Another 0.4s
    state = update_game(state, 0.4, 0.0)
    assert state.ball.animation_frame == 2
    
    # Wrap around
    state = update_game(state, 0.4, 0.0)
    assert state.ball.animation_frame == 0

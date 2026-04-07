from permanence_env.game.gameplay import init_game
from permanence_env.game.state import GameState, Ball, TargetRect

def test_init_game_state():
    """Verify init_game returns a valid initial state."""
    state = init_game()
    assert isinstance(state, GameState)
    assert isinstance(state.ball, Ball)
    assert isinstance(state.target, TargetRect)
    # Positions should be non-zero (highly likely)
    assert state.ball.mass > 0
    assert state.ball.friction >= 0

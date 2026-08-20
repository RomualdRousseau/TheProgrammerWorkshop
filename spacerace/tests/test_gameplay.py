"""Story 2 & 4 & 5: player rocket movement, collision, scoring, and timer.

Given/When/Then: a match state plus an input command produces the expected
new state, with no window or hardware involved.
"""

from dataclasses import replace
from unittest.mock import Mock

from spacerace.core import constant
from spacerace.core.input import InputCommand
from spacerace.core.render import RenderEngine
from spacerace.core.state import Player, PlayState
from spacerace.game import gameplay


def test_init_places_both_players_at_their_start_positions() -> None:
    state = gameplay.init()

    assert state.players[0] == Player(
        x=constant.P1_START_X, y=constant.START_Y, respawn_timer=0.0
    )
    assert state.players[1] == Player(
        x=constant.P2_START_X, y=constant.START_Y, respawn_timer=0.0
    )


def test_init_starts_with_zero_scores_and_full_timer() -> None:
    state = gameplay.init()

    assert state.scores == (0, 0)
    assert state.match_timer == constant.MATCH_DURATION


def test_player1_moves_up_with_its_key_while_player2_stays() -> None:
    # Given a fresh match
    state = gameplay.init()

    # When player 1 thrusts up for one second
    new_state = gameplay.update(InputCommand(p1_up=True), state, dt=1.0)

    # Then player 1 climbs by exactly its speed, player 2 is untouched
    assert new_state.players[0].y == constant.START_Y - constant.PLAYER_SPEED
    assert new_state.players[1] == state.players[1]


def test_player1_moves_down_with_its_key() -> None:
    state = gameplay.init()

    new_state = gameplay.update(InputCommand(p1_down=True), state, dt=0.1)

    assert new_state.players[0].y == constant.START_Y + constant.PLAYER_SPEED * 0.1


def test_player2_moves_independently_with_arrow_keys() -> None:
    state = gameplay.init()

    new_state = gameplay.update(InputCommand(p2_up=True), state, dt=1.0)

    assert new_state.players[1].y == constant.START_Y - constant.PLAYER_SPEED
    assert new_state.players[0] == state.players[0]


def test_movement_scales_with_dt() -> None:
    state = gameplay.init()

    new_state = gameplay.update(InputCommand(p1_up=True), state, dt=0.5)

    assert new_state.players[0].y == constant.START_Y - constant.PLAYER_SPEED * 0.5


def test_no_input_leaves_players_untouched_but_asteroids_move() -> None:
    state = gameplay.init()

    new_state = gameplay.update(InputCommand(), state, dt=1.0)

    assert new_state.players == state.players
    assert new_state.asteroids != state.asteroids


def test_pressing_both_directions_cancels_out() -> None:
    state = gameplay.init()

    new_state = gameplay.update(InputCommand(p1_up=True, p1_down=True), state, dt=1.0)

    assert new_state.players == state.players


def test_reaching_top_clamps_and_scores() -> None:
    # Given a rocket one pixel below the top edge
    state = PlayState(
        players=(
            Player(x=constant.P1_START_X, y=1.0, respawn_timer=0.0),
            gameplay.init().players[1],
        ),
        asteroids=gameplay.init().asteroids,
        rng_state=gameplay.init().rng_state,
        scores=(0, 0),
        match_timer=constant.MATCH_DURATION,
    )

    # When thrusting up for a long time
    new_state = gameplay.update(InputCommand(p1_up=True), state, dt=1.0)

    # Then it scores and resets at the start (it can never leave the field)
    assert new_state.scores[0] == 1
    assert new_state.players[0].y == constant.START_Y


def test_player_cannot_sink_below_the_field() -> None:
    max_y = float(constant.SCREEN_SIZE - constant.PLAYER_HEIGHT)
    state = PlayState(
        players=(
            Player(x=constant.P1_START_X, y=max_y - 1.0, respawn_timer=0.0),
            gameplay.init().players[1],
        ),
        asteroids=gameplay.init().asteroids,
        rng_state=gameplay.init().rng_state,
        scores=(0, 0),
        match_timer=constant.MATCH_DURATION,
    )

    new_state = gameplay.update(InputCommand(p1_down=True), state, dt=1.0)

    assert new_state.players[0].y == max_y


def test_draw_delegates_to_the_render_engine() -> None:
    render = Mock(spec=RenderEngine)
    state = gameplay.init()

    gameplay.draw(render, state)

    render.render_play.assert_called_once_with(state)


def test_render_engine_receives_hidden_player_state() -> None:
    # The game layer delegates the full state; hiding is the renderer's job.
    state = gameplay.init()
    state = replace(
        state,
        players=(
            replace(state.players[0], respawn_timer=constant.RESPAWN_DELAY),
            state.players[1],
        ),
    )
    render = Mock(spec=RenderEngine)

    gameplay.draw(render, state)

    render.render_play.assert_called_once_with(state)


def test_collision_hides_player_and_starts_respawn_timer() -> None:
    # Given a player positioned exactly over an asteroid
    state = gameplay.init(seed=42)
    asteroid = state.asteroids[0]
    player = Player(
        x=asteroid.x,
        y=asteroid.y,
        respawn_timer=0.0,
    )
    state = replace(
        state,
        players=(player, state.players[1]),
    )

    new_state = gameplay.update(InputCommand(), state, dt=0.0)

    assert new_state.players[0].respawn_timer == constant.RESPAWN_DELAY
    assert new_state.players[0].x == player.x
    assert new_state.players[0].y == player.y


def test_hidden_player_cannot_move() -> None:
    state = replace(
        gameplay.init(),
        players=(
            Player(x=constant.P1_START_X, y=constant.START_Y, respawn_timer=0.5),
            gameplay.init().players[1],
        ),
    )

    new_state = gameplay.update(InputCommand(p1_up=True), state, dt=0.1)

    assert new_state.players[0].x == constant.P1_START_X
    assert new_state.players[0].y == constant.START_Y


def test_hidden_player_does_not_collide() -> None:
    state = gameplay.init(seed=42)
    asteroid = state.asteroids[0]
    hidden_player = Player(
        x=asteroid.x,
        y=asteroid.y,
        respawn_timer=constant.RESPAWN_DELAY,
    )
    state = replace(
        state,
        players=(hidden_player, state.players[1]),
    )

    new_state = gameplay.update(InputCommand(), state, dt=0.0)

    assert new_state.players[0].respawn_timer == constant.RESPAWN_DELAY


def test_player_respawns_at_start_after_delay() -> None:
    state = replace(
        gameplay.init(),
        players=(
            Player(x=50.0, y=50.0, respawn_timer=0.3),
            gameplay.init().players[1],
        ),
    )

    new_state = gameplay.update(InputCommand(), state, dt=0.5)

    assert new_state.players[0].respawn_timer == 0.0
    assert new_state.players[0].x == constant.P1_START_X
    assert new_state.players[0].y == constant.START_Y


def test_hit_on_one_player_does_not_affect_the_other() -> None:
    state = gameplay.init(seed=42)
    asteroid = state.asteroids[0]
    hit_player = Player(x=asteroid.x, y=asteroid.y, respawn_timer=0.0)
    state = replace(
        state,
        players=(hit_player, state.players[1]),
    )

    new_state = gameplay.update(InputCommand(), state, dt=0.0)

    assert new_state.players[0].respawn_timer == constant.RESPAWN_DELAY
    assert new_state.players[1] == state.players[1]


def test_other_player_continues_while_one_is_hidden() -> None:
    state = replace(
        gameplay.init(),
        players=(
            Player(
                x=constant.P1_START_X,
                y=constant.START_Y,
                respawn_timer=constant.RESPAWN_DELAY,
            ),
            Player(x=constant.P2_START_X, y=constant.START_Y, respawn_timer=0.0),
        ),
    )

    new_state = gameplay.update(InputCommand(p2_up=True), state, dt=0.1)

    assert new_state.players[0].respawn_timer == constant.RESPAWN_DELAY - 0.1
    assert new_state.players[1].y == constant.START_Y - constant.PLAYER_SPEED * 0.1


def test_reaching_goal_row_increments_score_and_resets_player() -> None:
    state = replace(
        gameplay.init(),
        players=(
            Player(x=constant.P1_START_X, y=0.0, respawn_timer=0.0),
            gameplay.init().players[1],
        ),
        scores=(0, 5),
    )

    new_state = gameplay.update(InputCommand(), state, dt=0.0)

    assert new_state.scores == (1, 5)
    assert new_state.players[0].x == constant.P1_START_X
    assert new_state.players[0].y == constant.START_Y


def test_hidden_player_cannot_score() -> None:
    state = replace(
        gameplay.init(),
        players=(
            Player(x=constant.P1_START_X, y=0.0, respawn_timer=constant.RESPAWN_DELAY),
            gameplay.init().players[1],
        ),
    )

    new_state = gameplay.update(InputCommand(), state, dt=0.0)

    assert new_state.scores == (0, 0)


def test_match_timer_counts_down_each_frame() -> None:
    state = gameplay.init()

    new_state = gameplay.update(InputCommand(), state, dt=1.5)

    assert new_state.match_timer == constant.MATCH_DURATION - 1.5


def test_match_timer_clamps_at_zero() -> None:
    state = gameplay.init()

    new_state = gameplay.update(
        InputCommand(), state, dt=constant.MATCH_DURATION + 10.0
    )

    assert new_state.match_timer == 0.0


def test_scoring_does_not_affect_other_player() -> None:
    state = replace(
        gameplay.init(),
        players=(
            Player(x=constant.P1_START_X, y=0.0, respawn_timer=0.0),
            Player(x=constant.P2_START_X, y=100.0, respawn_timer=0.0),
        ),
    )

    new_state = gameplay.update(InputCommand(p2_up=True), state, dt=0.5)

    assert new_state.scores == (1, 0)
    assert new_state.players[1].y == 100.0 - constant.PLAYER_SPEED * 0.5

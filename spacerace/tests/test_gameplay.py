"""Story 2: player rocket movement and rendering — headless behavioral tests.

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


def test_player_cannot_fly_above_the_field() -> None:
    # Given a rocket one pixel below the top edge
    state = PlayState(
        players=(
            Player(x=constant.P1_START_X, y=1.0, respawn_timer=0.0),
            gameplay.init().players[1],
        ),
        asteroids=gameplay.init().asteroids,
        rng_state=gameplay.init().rng_state,
    )

    # When thrusting up for a long time
    new_state = gameplay.update(InputCommand(p1_up=True), state, dt=1.0)

    # Then it clamps at the top edge instead of leaving the field
    assert new_state.players[0].y == 0.0


def test_player_cannot_sink_below_the_field() -> None:
    max_y = float(constant.SCREEN_SIZE - constant.PLAYER_HEIGHT)
    state = PlayState(
        players=(
            Player(x=constant.P1_START_X, y=max_y - 1.0, respawn_timer=0.0),
            gameplay.init().players[1],
        ),
        asteroids=gameplay.init().asteroids,
        rng_state=gameplay.init().rng_state,
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
    state = PlayState(
        players=(player, state.players[1]),
        asteroids=state.asteroids,
        rng_state=state.rng_state,
    )

    new_state = gameplay.update(InputCommand(), state, dt=0.0)

    assert new_state.players[0].respawn_timer == constant.RESPAWN_DELAY
    assert new_state.players[0].x == player.x
    assert new_state.players[0].y == player.y


def test_hidden_player_cannot_move() -> None:
    state = PlayState(
        players=(
            Player(x=constant.P1_START_X, y=constant.START_Y, respawn_timer=0.5),
            gameplay.init().players[1],
        ),
        asteroids=gameplay.init().asteroids,
        rng_state=gameplay.init().rng_state,
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
    state = PlayState(
        players=(hidden_player, state.players[1]),
        asteroids=state.asteroids,
        rng_state=state.rng_state,
    )

    new_state = gameplay.update(InputCommand(), state, dt=0.0)

    assert new_state.players[0].respawn_timer == constant.RESPAWN_DELAY


def test_player_respawns_at_start_after_delay() -> None:
    state = PlayState(
        players=(
            Player(x=50.0, y=50.0, respawn_timer=0.3),
            gameplay.init().players[1],
        ),
        asteroids=gameplay.init().asteroids,
        rng_state=gameplay.init().rng_state,
    )

    new_state = gameplay.update(InputCommand(), state, dt=0.5)

    assert new_state.players[0].respawn_timer == 0.0
    assert new_state.players[0].x == constant.P1_START_X
    assert new_state.players[0].y == constant.START_Y


def test_hit_on_one_player_does_not_affect_the_other() -> None:
    state = gameplay.init(seed=42)
    asteroid = state.asteroids[0]
    hit_player = Player(x=asteroid.x, y=asteroid.y, respawn_timer=0.0)
    state = PlayState(
        players=(hit_player, state.players[1]),
        asteroids=state.asteroids,
        rng_state=state.rng_state,
    )

    new_state = gameplay.update(InputCommand(), state, dt=0.0)

    assert new_state.players[0].respawn_timer == constant.RESPAWN_DELAY
    assert new_state.players[1] == state.players[1]


def test_other_player_continues_while_one_is_hidden() -> None:
    state = PlayState(
        players=(
            Player(
                x=constant.P1_START_X,
                y=constant.START_Y,
                respawn_timer=constant.RESPAWN_DELAY,
            ),
            Player(x=constant.P2_START_X, y=constant.START_Y, respawn_timer=0.0),
        ),
        asteroids=gameplay.init().asteroids,
        rng_state=gameplay.init().rng_state,
    )

    new_state = gameplay.update(InputCommand(p2_up=True), state, dt=0.1)

    assert new_state.players[0].respawn_timer == constant.RESPAWN_DELAY - 0.1
    assert new_state.players[1].y == constant.START_Y - constant.PLAYER_SPEED * 0.1

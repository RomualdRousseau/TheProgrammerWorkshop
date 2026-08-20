"""Story 9: ship engine beeps — pure altitude→progress mapping and audio state."""

from spacerace.core import constant
from spacerace.core.audio import ship_altitude_progress
from spacerace.core.input import InputCommand
from spacerace.core.state import (
    AppState,
    AudioState,
    GameOverState,
    Player,
    PlayState,
    Scene,
)
from spacerace.game import scenes


def test_progress_is_zero_at_start_row() -> None:
    y = constant.START_Y + constant.PLAYER_HEIGHT / 2.0
    assert ship_altitude_progress(y) == 0.0


def test_progress_is_one_at_goal_row() -> None:
    y = constant.GOAL_ROW + constant.PLAYER_HEIGHT / 2.0
    assert ship_altitude_progress(y) == 1.0


def test_progress_is_mid_at_halfway() -> None:
    bottom = constant.START_Y + constant.PLAYER_HEIGHT / 2.0
    top = constant.GOAL_ROW + constant.PLAYER_HEIGHT / 2.0
    y = (bottom + top) / 2.0
    assert ship_altitude_progress(y) == 0.5


def test_progress_clamps_below_zero() -> None:
    y = constant.START_Y + constant.PLAYER_HEIGHT * 2.0
    assert ship_altitude_progress(y) == 0.0


def test_progress_clamps_above_one() -> None:
    y = constant.GOAL_ROW - constant.PLAYER_HEIGHT
    assert ship_altitude_progress(y) == 1.0


def test_audio_state_is_silent_on_title() -> None:
    state = scenes.init()

    assert scenes.audio_state(state) == AudioState(p1_progress=None, p2_progress=None)


def test_audio_state_is_silent_on_gameover() -> None:
    play = scenes.update(InputCommand(confirm=True), scenes.init(), dt=0.0).play
    assert play is not None
    state = AppState(
        scene=Scene.GAMEOVER,
        title=None,
        play=None,
        gameover=GameOverState(final_state=play, timeout=constant.GAMEOVER_TIMEOUT),
        demo=None,
    )

    assert scenes.audio_state(state) == AudioState(p1_progress=None, p2_progress=None)


def test_audio_state_active_for_both_players_in_match() -> None:
    play = scenes.update(InputCommand(confirm=True), scenes.init(), dt=0.0).play
    assert play is not None
    state = AppState(
        scene=Scene.PLAYING,
        title=None,
        play=play,
        gameover=None,
        demo=None,
    )

    audio = scenes.audio_state(state)

    assert audio.p1_progress is not None
    assert audio.p2_progress is not None
    assert 0.0 <= audio.p1_progress <= 1.0
    assert 0.0 <= audio.p2_progress <= 1.0


def test_audio_state_mutes_hidden_player() -> None:
    play = scenes.update(InputCommand(confirm=True), scenes.init(), dt=0.0).play
    assert play is not None
    hidden = Player(
        x=play.players[0].x,
        y=play.players[0].y,
        respawn_timer=constant.RESPAWN_DELAY,
    )
    state = AppState(
        scene=Scene.PLAYING,
        title=None,
        play=PlayState(
            players=(hidden, play.players[1]),
            asteroids=play.asteroids,
            rng_state=play.rng_state,
            scores=play.scores,
            match_timer=play.match_timer,
        ),
        gameover=None,
        demo=None,
    )

    audio = scenes.audio_state(state)

    assert audio.p1_progress is None
    assert audio.p2_progress is not None


def test_audio_state_active_in_demo() -> None:
    demo_state = scenes.update(
        InputCommand(), scenes.init(), dt=constant.TITLE_INACTIVITY_TIMEOUT
    )
    assert demo_state.scene == Scene.DEMO
    assert demo_state.demo is not None

    audio = scenes.audio_state(demo_state)

    assert audio.p1_progress is not None
    assert audio.p2_progress is not None


def test_audio_state_progress_changes_with_altitude() -> None:
    play = scenes.update(InputCommand(confirm=True), scenes.init(), dt=0.0).play
    assert play is not None
    low = AppState(
        scene=Scene.PLAYING,
        title=None,
        play=play,
        gameover=None,
        demo=None,
    )
    high_play = PlayState(
        players=(
            Player(x=play.players[0].x, y=constant.GOAL_ROW, respawn_timer=0.0),
            play.players[1],
        ),
        asteroids=play.asteroids,
        rng_state=play.rng_state,
        scores=play.scores,
        match_timer=play.match_timer,
    )
    high = AppState(
        scene=Scene.PLAYING,
        title=None,
        play=high_play,
        gameover=None,
        demo=None,
    )

    low_audio = scenes.audio_state(low)
    high_audio = scenes.audio_state(high)

    assert low_audio.p1_progress is not None
    assert high_audio.p1_progress is not None
    assert high_audio.p1_progress > low_audio.p1_progress

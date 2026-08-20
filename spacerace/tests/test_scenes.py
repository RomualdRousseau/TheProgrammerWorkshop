"""Story 6 & 7: title screen, scene router, and game over — headless tests."""

from dataclasses import replace
from unittest.mock import Mock

from spacerace.core import constant
from spacerace.core.input import InputCommand
from spacerace.core.render import RenderEngine
from spacerace.core.state import AppState, GameOverState, Scene
from spacerace.game import scenes


def test_init_boots_into_title_screen() -> None:
    state = scenes.init()

    assert state.scene == Scene.TITLE
    assert state.title is not None
    assert state.title.inactivity_timer == constant.TITLE_INACTIVITY_TIMEOUT
    assert state.play is None
    assert state.gameover is None


def test_confirm_on_title_starts_a_fresh_match() -> None:
    state = scenes.init()

    new_state = scenes.update(InputCommand(confirm=True), state, dt=0.0)

    assert new_state.scene == Scene.PLAYING
    assert new_state.play is not None
    assert new_state.play.scores == (0, 0)
    assert new_state.play.match_timer == constant.MATCH_DURATION
    assert new_state.gameover is None


def test_title_inactivity_timer_counts_down() -> None:
    state = scenes.init()

    new_state = scenes.update(InputCommand(), state, dt=1.0)

    assert new_state.scene == Scene.TITLE
    assert new_state.title is not None
    assert new_state.title.inactivity_timer == constant.TITLE_INACTIVITY_TIMEOUT - 1.0


def test_title_inactivity_clamps_at_zero() -> None:
    state = scenes.init()

    new_state = scenes.update(
        InputCommand(), state, dt=constant.TITLE_INACTIVITY_TIMEOUT + 5.0
    )

    assert new_state.scene == Scene.TITLE
    assert new_state.title is not None
    assert new_state.title.inactivity_timer == 0.0


def test_any_movement_key_resets_title_inactivity() -> None:
    state = scenes.update(InputCommand(), scenes.init(), dt=5.0)
    assert state.title is not None
    assert state.title.inactivity_timer < constant.TITLE_INACTIVITY_TIMEOUT

    new_state = scenes.update(InputCommand(p1_up=True), state, dt=0.0)

    assert new_state.scene == Scene.TITLE
    assert new_state.title is not None
    assert new_state.title.inactivity_timer == constant.TITLE_INACTIVITY_TIMEOUT


def test_playing_scene_advances_the_match() -> None:
    play_state = scenes.update(InputCommand(confirm=True), scenes.init(), dt=0.0).play
    assert play_state is not None
    state = AppState(scene=Scene.PLAYING, title=None, play=play_state, gameover=None)

    new_state = scenes.update(InputCommand(p1_up=True), state, dt=1.0)

    assert new_state.scene == Scene.PLAYING
    assert new_state.play is not None
    assert new_state.play.players[0].y < constant.START_Y


def test_title_draw_delegates_to_render_engine() -> None:
    render = Mock(spec=RenderEngine)
    state = scenes.init()

    scenes.draw(render, state)

    render.render_title.assert_called_once_with(state.title)


def test_playing_draw_uses_render_texture_lifecycle() -> None:
    render = Mock(spec=RenderEngine)
    play_state = scenes.update(InputCommand(confirm=True), scenes.init(), dt=0.0).play
    assert play_state is not None
    state = AppState(scene=Scene.PLAYING, title=None, play=play_state, gameover=None)

    scenes.draw(render, state)

    render.begin_frame.assert_called_once()
    render.render_play.assert_called_once_with(play_state)
    render.end_frame.assert_called_once()


def test_match_timer_expiry_transitions_to_gameover() -> None:
    play_state = scenes.update(InputCommand(confirm=True), scenes.init(), dt=0.0).play
    assert play_state is not None
    state = AppState(scene=Scene.PLAYING, title=None, play=play_state, gameover=None)

    new_state = scenes.update(InputCommand(), state, dt=constant.MATCH_DURATION)

    assert new_state.scene == Scene.GAMEOVER
    assert new_state.gameover is not None
    assert new_state.gameover.final_state.match_timer == 0.0


def test_gameover_timeout_returns_to_title() -> None:
    play_state = scenes.update(InputCommand(confirm=True), scenes.init(), dt=0.0).play
    assert play_state is not None
    state = AppState(scene=Scene.PLAYING, title=None, play=play_state, gameover=None)
    gameover_state = scenes.update(InputCommand(), state, dt=constant.MATCH_DURATION)
    assert gameover_state.scene == Scene.GAMEOVER
    assert gameover_state.gameover is not None

    new_state = scenes.update(
        InputCommand(), gameover_state, dt=constant.GAMEOVER_TIMEOUT
    )

    assert new_state.scene == Scene.TITLE
    assert new_state.title is not None


def test_confirm_on_gameover_returns_to_title() -> None:
    play_state = scenes.update(InputCommand(confirm=True), scenes.init(), dt=0.0).play
    assert play_state is not None
    state = AppState(scene=Scene.PLAYING, title=None, play=play_state, gameover=None)
    gameover_state = scenes.update(InputCommand(), state, dt=constant.MATCH_DURATION)
    assert gameover_state.gameover is not None

    new_state = scenes.update(InputCommand(confirm=True), gameover_state, dt=0.0)

    assert new_state.scene == Scene.TITLE


def test_gameover_timeout_is_independent_of_match_timer() -> None:
    final_state = (
        replace(
            play_state,
            match_timer=0.0,
        )
        if (
            play_state := scenes.update(
                InputCommand(confirm=True), scenes.init(), dt=0.0
            ).play
        )
        is not None
        else None
    )
    assert final_state is not None
    state = AppState(
        scene=Scene.GAMEOVER,
        title=None,
        play=None,
        gameover=GameOverState(
            final_state=final_state, timeout=constant.GAMEOVER_TIMEOUT
        ),
    )

    new_state = scenes.update(InputCommand(), state, dt=0.0)

    assert new_state.scene == Scene.GAMEOVER
    assert new_state.gameover is not None
    assert new_state.gameover.timeout == constant.GAMEOVER_TIMEOUT


def test_new_match_from_title_after_gameover_resets_everything() -> None:
    play_state = scenes.update(InputCommand(confirm=True), scenes.init(), dt=0.0).play
    assert play_state is not None
    playing = AppState(scene=Scene.PLAYING, title=None, play=play_state, gameover=None)
    gameover = scenes.update(InputCommand(), playing, dt=constant.MATCH_DURATION)
    assert gameover.scene == Scene.GAMEOVER
    title = scenes.update(InputCommand(confirm=True), gameover, dt=0.0)
    assert title.scene == Scene.TITLE

    new_match = scenes.update(InputCommand(confirm=True), title, dt=0.0)

    assert new_match.scene == Scene.PLAYING
    assert new_match.play is not None
    assert new_match.play.scores == (0, 0)
    assert new_match.play.match_timer == constant.MATCH_DURATION


def test_gameover_draw_renders_frozen_final_frame() -> None:
    render = Mock(spec=RenderEngine)
    play_state = scenes.update(InputCommand(confirm=True), scenes.init(), dt=0.0).play
    assert play_state is not None
    playing = AppState(scene=Scene.PLAYING, title=None, play=play_state, gameover=None)
    gameover = scenes.update(InputCommand(), playing, dt=constant.MATCH_DURATION)
    assert gameover.gameover is not None

    scenes.draw(render, gameover)

    render.begin_frame.assert_called_once()
    render.render_play.assert_called_once_with(gameover.gameover.final_state)
    render.end_frame.assert_called_once()

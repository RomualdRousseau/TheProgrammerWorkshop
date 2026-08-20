"""Story 6: title screen and scene router — headless behavioral tests."""

from unittest.mock import Mock

from spacerace.core import constant
from spacerace.core.input import InputCommand
from spacerace.core.render import RenderEngine
from spacerace.core.state import AppState, Scene
from spacerace.game import scenes


def test_init_boots_into_title_screen() -> None:
    state = scenes.init()

    assert state.scene == Scene.TITLE
    assert state.title is not None
    assert state.title.inactivity_timer == constant.TITLE_INACTIVITY_TIMEOUT
    assert state.play is None


def test_confirm_on_title_starts_a_fresh_match() -> None:
    state = scenes.init()

    new_state = scenes.update(InputCommand(confirm=True), state, dt=0.0)

    assert new_state.scene == Scene.PLAYING
    assert new_state.play is not None
    assert new_state.play.scores == (0, 0)
    assert new_state.play.match_timer == constant.MATCH_DURATION


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
    state = AppState(scene=Scene.PLAYING, title=None, play=play_state)

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
    state = AppState(scene=Scene.PLAYING, title=None, play=play_state)

    scenes.draw(render, state)

    render.begin_frame.assert_called_once()
    render.render_play.assert_called_once_with(play_state)
    render.end_frame.assert_called_once()

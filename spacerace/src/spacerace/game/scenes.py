"""Scene router: dispatches update and draw between Title, Playing, Game Over."""

from collections.abc import Callable
from dataclasses import dataclass

from spacerace.core import constant
from spacerace.core.input import InputCommand
from spacerace.core.render import RenderEngine
from spacerace.core.state import (
    AppState,
    GameOverState,
    Scene,
    TitleState,
)
from spacerace.game import gameplay


@dataclass(slots=True, frozen=True)
class _SceneHandlers:
    """Update/draw pair for a single scene."""

    update: Callable[[InputCommand, AppState, float], AppState]
    draw: Callable[[RenderEngine, AppState], None]


def init() -> AppState:
    """Boot into the title screen."""
    return AppState(
        scene=Scene.TITLE,
        title=TitleState(inactivity_timer=constant.TITLE_INACTIVITY_TIMEOUT),
        play=None,
        gameover=None,
    )


def update(command: InputCommand, state: AppState, dt: float) -> AppState:
    """Dispatch update to the active scene via the transition table."""
    handlers = _SCENE_TABLE.get(state.scene)
    if handlers is None:
        return state
    return handlers.update(command, state, dt)


def draw(render: RenderEngine, state: AppState) -> None:
    """Dispatch draw to the active scene via the transition table."""
    handlers = _SCENE_TABLE.get(state.scene)
    if handlers is not None:
        handlers.draw(render, state)


def _draw_title(render: RenderEngine, state: AppState) -> None:
    assert state.title is not None
    render.render_title(state.title)


def _draw_playing(render: RenderEngine, state: AppState) -> None:
    assert state.play is not None
    render.begin_frame()
    gameplay.draw(render, state.play)
    render.end_frame()


def _draw_gameover(render: RenderEngine, state: AppState) -> None:
    assert state.gameover is not None
    render.begin_frame()
    gameplay.draw(render, state.gameover.final_state)
    render.end_frame()


def _go_to_title() -> AppState:
    """Return a fresh title screen state."""
    return AppState(
        scene=Scene.TITLE,
        title=TitleState(inactivity_timer=constant.TITLE_INACTIVITY_TIMEOUT),
        play=None,
        gameover=None,
    )


def _update_title(command: InputCommand, state: AppState, dt: float) -> AppState:
    """Handle title input and inactivity timer."""
    title = state.title
    if title is None:
        title = TitleState(inactivity_timer=constant.TITLE_INACTIVITY_TIMEOUT)

    if command.confirm:
        return AppState(
            scene=Scene.PLAYING,
            title=None,
            play=gameplay.init(),
            gameover=None,
        )

    if _any_mapped_key(command):
        return _go_to_title()

    return AppState(
        scene=Scene.TITLE,
        title=TitleState(inactivity_timer=max(0.0, title.inactivity_timer - dt)),
        play=None,
        gameover=None,
    )


def _update_playing(command: InputCommand, state: AppState, dt: float) -> AppState:
    """Advance the live match; transition to Game Over when time expires."""
    play = state.play
    if play is None:
        play = gameplay.init()
    new_play = gameplay.update(command, play, dt)
    if new_play.match_timer <= 0:
        return AppState(
            scene=Scene.GAMEOVER,
            title=None,
            play=None,
            gameover=GameOverState(
                final_state=new_play,
                timeout=constant.GAMEOVER_TIMEOUT,
            ),
        )
    return AppState(
        scene=Scene.PLAYING,
        title=None,
        play=new_play,
        gameover=None,
    )


def _update_gameover(command: InputCommand, state: AppState, dt: float) -> AppState:
    """Return to title on Space or after the game-over timeout."""
    gameover = state.gameover
    if gameover is None:
        gameover = GameOverState(
            final_state=gameplay.init(), timeout=constant.GAMEOVER_TIMEOUT
        )

    if command.confirm:
        return _go_to_title()

    new_timeout = gameover.timeout - dt
    if new_timeout <= 0:
        return _go_to_title()

    return AppState(
        scene=Scene.GAMEOVER,
        title=None,
        play=None,
        gameover=GameOverState(
            final_state=gameover.final_state,
            timeout=new_timeout,
        ),
    )


def _any_mapped_key(command: InputCommand) -> bool:
    """Return True for any player movement key (confirm is handled separately)."""
    return command.p1_up or command.p1_down or command.p2_up or command.p2_down


_SCENE_TABLE: dict[Scene, _SceneHandlers] = {
    Scene.TITLE: _SceneHandlers(update=_update_title, draw=_draw_title),
    Scene.PLAYING: _SceneHandlers(update=_update_playing, draw=_draw_playing),
    Scene.GAMEOVER: _SceneHandlers(update=_update_gameover, draw=_draw_gameover),
}

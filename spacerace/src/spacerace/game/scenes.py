"""Scene router: dispatches update and draw between Title, Playing, Game Over."""

from spacerace.core import constant
from spacerace.core.input import InputCommand
from spacerace.core.render import RenderEngine
from spacerace.core.state import (
    AppState,
    GameOverState,
    PlayState,
    Scene,
    TitleState,
)
from spacerace.game import gameplay


def init() -> AppState:
    """Boot into the title screen."""
    return AppState(
        scene=Scene.TITLE,
        title=TitleState(inactivity_timer=constant.TITLE_INACTIVITY_TIMEOUT),
        play=None,
        gameover=None,
    )


def update(command: InputCommand, state: AppState, dt: float) -> AppState:
    """Dispatch update to the active scene."""
    if state.scene == Scene.TITLE:
        return _update_title(command, state.title, dt)
    if state.scene == Scene.PLAYING:
        return _update_playing(command, state.play, dt)
    if state.scene == Scene.GAMEOVER:
        return _update_gameover(command, state.gameover, dt)
    return state


def draw(render: RenderEngine, state: AppState) -> None:
    """Dispatch draw to the active scene, handling frame lifecycle per scene."""
    if state.scene == Scene.TITLE:
        assert state.title is not None
        render.render_title(state.title)
    elif state.scene == Scene.PLAYING:
        assert state.play is not None
        render.begin_frame()
        gameplay.draw(render, state.play)
        render.end_frame()
    elif state.scene == Scene.GAMEOVER:
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


def _update_title(
    command: InputCommand, title: TitleState | None, dt: float
) -> AppState:
    """Handle title input and inactivity timer."""
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


def _update_playing(
    command: InputCommand, play: PlayState | None, dt: float
) -> AppState:
    """Advance the live match; transition to Game Over when time expires."""
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


def _update_gameover(
    command: InputCommand, gameover: GameOverState | None, dt: float
) -> AppState:
    """Return to title on Space or after the game-over timeout."""
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

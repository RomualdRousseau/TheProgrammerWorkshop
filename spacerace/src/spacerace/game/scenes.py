"""Scene router: dispatches update and draw between Title, Playing, Game Over, Demo."""

import random
from collections.abc import Callable
from dataclasses import dataclass

from spacerace.core import constant
from spacerace.core.audio import ship_altitude_progress
from spacerace.core.input import InputCommand
from spacerace.core.render import RenderEngine
from spacerace.core.state import (
    AppState,
    AudioState,
    DemoState,
    GameOverState,
    PlayState,
    Scene,
    TitleState,
)
from spacerace.game import gameplay
from spacerace.game.random_bot import RandomBot


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
        demo=None,
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


def audio_state(state: AppState) -> AudioState:
    """Derive the high-level audio representation from the current scene."""
    play = _active_play_state(state)
    if play is None:
        return AudioState(p1_progress=None, p2_progress=None)

    p1, p2 = play.players
    return AudioState(
        p1_progress=ship_altitude_progress(p1.y) if p1.respawn_timer == 0 else None,
        p2_progress=ship_altitude_progress(p2.y) if p2.respawn_timer == 0 else None,
    )


def _active_play_state(state: AppState) -> PlayState | None:
    """Return the live PlayState for active matches, None otherwise."""
    if state.scene == Scene.PLAYING:
        return state.play
    if state.scene == Scene.DEMO and state.demo is not None:
        return state.demo.play
    return None


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


def _draw_demo(render: RenderEngine, state: AppState) -> None:
    assert state.demo is not None
    render.begin_frame()
    gameplay.draw(render, state.demo.play)
    render.end_frame()


def _go_to_title() -> AppState:
    """Return a fresh title screen state."""
    return AppState(
        scene=Scene.TITLE,
        title=TitleState(inactivity_timer=constant.TITLE_INACTIVITY_TIMEOUT),
        play=None,
        gameover=None,
        demo=None,
    )


def _go_to_demo() -> AppState:
    """Return a fresh demo/attract-loop state."""
    return AppState(
        scene=Scene.DEMO,
        title=None,
        play=None,
        gameover=None,
        demo=DemoState(
            play=gameplay.init(),
            remaining=constant.DEMO_DURATION,
            bot=RandomBot(seed=random.randint(0, 2_147_483_647)),
        ),
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
            demo=None,
        )

    if _any_mapped_key(command):
        return _go_to_title()

    new_timer = title.inactivity_timer - dt
    if new_timer <= 0:
        return _go_to_demo()

    return AppState(
        scene=Scene.TITLE,
        title=TitleState(inactivity_timer=new_timer),
        play=None,
        gameover=None,
        demo=None,
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
            demo=None,
        )
    return AppState(
        scene=Scene.PLAYING,
        title=None,
        play=new_play,
        gameover=None,
        demo=None,
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
        demo=None,
    )


def _update_demo(command: InputCommand, state: AppState, dt: float) -> AppState:
    """Run the attract loop; Space starts a real match, timeout returns to title."""
    demo = state.demo
    if demo is None:
        return _go_to_demo()

    if command.confirm:
        return AppState(
            scene=Scene.PLAYING,
            title=None,
            play=gameplay.init(),
            gameover=None,
            demo=None,
        )

    new_remaining = demo.remaining - dt
    if new_remaining <= 0:
        return _go_to_title()

    return AppState(
        scene=Scene.DEMO,
        title=None,
        play=None,
        gameover=None,
        demo=DemoState(
            play=gameplay.update(command, demo.play, dt),
            remaining=new_remaining,
            bot=demo.bot,
        ),
    )


def _any_mapped_key(command: InputCommand) -> bool:
    """Return True for any player movement key (confirm is handled separately)."""
    return command.p1_up or command.p1_down or command.p2_up or command.p2_down


_SCENE_TABLE: dict[Scene, _SceneHandlers] = {
    Scene.TITLE: _SceneHandlers(update=_update_title, draw=_draw_title),
    Scene.PLAYING: _SceneHandlers(update=_update_playing, draw=_draw_playing),
    Scene.GAMEOVER: _SceneHandlers(update=_update_gameover, draw=_draw_gameover),
    Scene.DEMO: _SceneHandlers(update=_update_demo, draw=_draw_demo),
}

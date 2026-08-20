"""The live match: two rockets racing upward. Pure logic, engine-agnostic."""

import random
from dataclasses import replace

from spacerace.core import constant
from spacerace.core.input import InputCommand
from spacerace.core.physics import (
    collides,
    make_asteroids,
    move_player,
    update_asteroids,
)
from spacerace.core.render import RenderEngine
from spacerace.core.state import Asteroid, Player, PlayState


def init(seed: int | None = None) -> PlayState:
    """Start a fresh match: both rockets at their launch pads.

    A fixed ``seed`` makes the asteroid layout deterministic; ``None`` uses a
    random seed for production play.
    """
    rng_state = random.Random(seed).getstate()
    asteroids, rng_state = make_asteroids(rng_state)
    return PlayState(
        players=(
            Player(x=constant.P1_START_X, y=constant.START_Y, respawn_timer=0.0),
            Player(x=constant.P2_START_X, y=constant.START_Y, respawn_timer=0.0),
        ),
        asteroids=asteroids,
        rng_state=rng_state,
    )


def update(command: InputCommand, state: PlayState, dt: float) -> PlayState:
    """Advance the match by one frame, applying both players' intentions."""
    asteroids, rng_state = update_asteroids(state.asteroids, state.rng_state, dt)
    player1 = _update_player(
        state.players[0],
        command.p1_up,
        command.p1_down,
        dt,
        constant.P1_START_X,
        asteroids,
    )
    player2 = _update_player(
        state.players[1],
        command.p2_up,
        command.p2_down,
        dt,
        constant.P2_START_X,
        asteroids,
    )
    return replace(
        state, players=(player1, player2), asteroids=asteroids, rng_state=rng_state
    )


def draw(render: RenderEngine, state: PlayState) -> None:
    """Ask the engine to render the match representation."""
    render.render_play(state)


def _thrust(up: bool, down: bool) -> float:
    """Convert keys to a signed vertical velocity: up is negative (screen y)."""
    return (float(down) - float(up)) * constant.PLAYER_SPEED


def _update_player(
    player: Player,
    up: bool,
    down: bool,
    dt: float,
    start_x: float,
    asteroids: tuple[Asteroid, ...],
) -> Player:
    """Move one player, handle hits, and count down respawn timers."""
    if player.respawn_timer > 0:
        new_timer = player.respawn_timer - dt
        if new_timer <= 0:
            return Player(x=start_x, y=constant.START_Y, respawn_timer=0.0)
        return replace(player, respawn_timer=new_timer)

    moved = move_player(player, _thrust(up, down), dt)
    if any(collides(moved, asteroid) for asteroid in asteroids):
        return replace(moved, respawn_timer=constant.RESPAWN_DELAY)
    return moved

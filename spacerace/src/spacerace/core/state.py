"""World state: immutable dataclasses describing the Space Race universe."""

from dataclasses import dataclass
from enum import Enum


class Scene(Enum):
    """Top-level application scenes."""

    TITLE = "title"
    PLAYING = "playing"
    GAMEOVER = "gameover"


@dataclass(slots=True, frozen=True)
class Player:
    """A rocket. Position is the sprite's top-left corner in logical pixels.

    ``respawn_timer`` counts down while the rocket is hidden after a hit;
    when it is zero the rocket is active.
    """

    x: float
    y: float
    respawn_timer: float


@dataclass(slots=True, frozen=True)
class Asteroid:
    """A horizontal obstacle: a vertical bar that sweeps across a lane."""

    x: float
    y: float
    width: int
    height: int
    velocity_x: float


@dataclass(slots=True, frozen=True)
class PlayState:
    """Everything a live match owns."""

    players: tuple[Player, Player]
    asteroids: tuple[Asteroid, ...]
    rng_state: tuple  # random.Random state for deterministic respawns
    scores: tuple[int, int]
    match_timer: float


@dataclass(slots=True, frozen=True)
class TitleState:
    """Data tracked while the title screen is shown."""

    inactivity_timer: float


@dataclass(slots=True, frozen=True)
class GameOverState:
    """Frozen final match state plus the automatic return timeout."""

    final_state: PlayState
    timeout: float


@dataclass(slots=True, frozen=True)
class AppState:
    """The scene router's state: one active scene plus its payload."""

    scene: Scene
    title: TitleState | None
    play: PlayState | None
    gameover: GameOverState | None

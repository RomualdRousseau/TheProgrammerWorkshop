"""World state: immutable dataclasses describing the Space Race universe."""

from dataclasses import dataclass


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

"""World state: immutable dataclasses describing the Space Race universe."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Player:
    """A rocket. Position is the sprite's top-left corner in logical pixels."""

    x: float
    y: float


@dataclass(slots=True, frozen=True)
class PlayState:
    """Everything a live match owns."""

    players: tuple[Player, Player]

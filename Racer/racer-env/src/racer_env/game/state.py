from dataclasses import dataclass, field

import pyray as pr


@dataclass
class Entity:
    """Represents any object in the game world."""

    position: pr.Vector2
    velocity: pr.Vector2
    width: float
    height: float

    @property
    def rect(self) -> pr.Rectangle:
        """Returns the collision rectangle for the entity."""
        return pr.Rectangle(self.position.x, self.position.y, self.width, self.height)


@dataclass
class GameState:
    """Holds the entire state of the racing simulation."""

    player: Entity
    obstacles: list[Entity] = field(default_factory=list)
    score: int = 0
    timer: float = 0.0
    game_over: bool = False
    won: bool = False
    spawn_timer: float = 0.0

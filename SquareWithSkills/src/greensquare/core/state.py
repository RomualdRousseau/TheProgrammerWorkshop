"""Data state containers for player and input."""

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class InputState:
    move_x: float = 0.0  # -1.0 (left), 0.0, 1.0 (right)
    move_y: float = 0.0  # -1.0 (up), 0.0, 1.0 (down)
    should_quit: bool = False


@dataclass(slots=True, frozen=True)
class PlayerState:
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    trail: tuple[tuple[float, float], ...] = field(default_factory=tuple)

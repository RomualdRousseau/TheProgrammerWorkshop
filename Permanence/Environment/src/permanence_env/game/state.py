"""
State definitions for the game domain.
"""

from dataclasses import dataclass
import pyray as pr


@dataclass
class Ball:
    """
    Represents the physical ball in the simulation.
    """

    pos: pr.Vector2
    velocity: pr.Vector2
    mass: float
    friction: float
    radius: float = 0.0
    animation_frame: int = 0
    animation_timer: float = 0.0


@dataclass
class TargetRect:
    """
    Represents the target rectangle in grid coordinates and its specific target point.
    """

    grid_x: int  # Top-left grid X
    grid_y: int  # Top-left grid Y
    wp1_pos: pr.Vector2  # Specific point inside the rectangle


@dataclass
class GameState:
    """
    Root container for the entire simulation state.
    """

    ball: Ball
    target: TargetRect
    show_layer2: bool = True

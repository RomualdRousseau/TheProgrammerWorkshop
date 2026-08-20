"""Input abstraction: what the game needs to know, decoupled from hardware."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True, frozen=True)
class InputCommand:
    """One frame of intentions for both players plus the confirm key."""

    p1_up: bool = False
    p1_down: bool = False
    p2_up: bool = False
    p2_down: bool = False
    confirm: bool = False  # edge-triggered Space


class InputSource(Protocol):
    """Anything that can produce per-frame commands: keyboard, bots, scripts."""

    def poll(self, dt: float) -> InputCommand:
        """Return the command for the current frame; dt lets sources pace themselves."""
        ...

"""Render abstraction: high-level, semantic representations only.

The game layer never issues primitive draw calls; it asks the engine to
render a whole scene representation. This keeps the game layer headless
and leaves the engine free to polish visuals independently.
"""

from typing import Protocol

from spacerace.core.state import PlayState, TitleState


class RenderEngine(Protocol):
    """The frame-loop and scene-rendering surface the game relies on."""

    def should_quit(self) -> bool:
        """Return True when the user asks to quit."""
        ...

    def get_frame_time(self) -> float:
        """Return the elapsed time in seconds since the previous frame."""
        ...

    def begin_frame(self) -> None:
        """Start drawing the world into the low-resolution target."""
        ...

    def end_frame(self) -> None:
        """Upscale the target to the window and present it."""
        ...

    def render_play(self, state: PlayState) -> None:
        """Render a live match: rockets, obstacles, HUD."""
        ...

    def render_title(self, state: TitleState) -> None:
        """Render the title screen at native window resolution."""
        ...

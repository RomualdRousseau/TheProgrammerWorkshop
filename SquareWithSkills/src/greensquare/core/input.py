"""Input engine protocol specification."""

from typing import Protocol
from greensquare.core.state import InputState


class InputEngine(Protocol):
    def poll_input(self) -> InputState: ...

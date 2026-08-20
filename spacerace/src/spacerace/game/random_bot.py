"""A deterministic, replaceable bot InputSource for the attract-loop demo."""

import random

from spacerace.core.input import InputCommand


class RandomBot:
    """Auto-pilot that flips movement keys every decision interval.

    ``confirm`` is always False so the bot never leaves the demo scene.
    A fixed ``seed`` makes the command stream deterministic.
    """

    _DECISION_INTERVAL: float = 0.15

    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)
        self._timer: float = 0.0
        self._command: InputCommand = self._new_command()

    def poll(self, dt: float) -> InputCommand:
        """Return the current command, re-rolling it at each interval."""
        self._timer += dt
        if self._timer >= self._DECISION_INTERVAL:
            self._timer -= self._DECISION_INTERVAL
            self._command = self._new_command()
        return self._command

    def _new_command(self) -> InputCommand:
        return InputCommand(
            p1_up=self._rng.choice((True, False)),
            p1_down=self._rng.choice((True, False)),
            p2_up=self._rng.choice((True, False)),
            p2_down=self._rng.choice((True, False)),
            confirm=False,
        )

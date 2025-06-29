from typing import Protocol


class Quest(Protocol):
    def is_completed(self) -> bool: ...

    def process_next_state(self, game): ...

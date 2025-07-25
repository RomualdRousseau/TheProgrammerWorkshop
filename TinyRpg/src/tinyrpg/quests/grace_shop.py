from typing import Any, Protocol

from tinyrpg.engine import Character, Particle, VerticalEffect, Widget
from tinyrpg.widgets import ShoppingCart


class Game(Protocol):
    player: Character
    particles: list[Particle] = []
    widgets: list[Widget] = []


class GraceShop:
    def __init__(self):
        self.quest_name = "Grace's Shop"
        self.quest_description = "Grace sells and buys stuffs."

    def reset(self):
        pass

    def is_assignable(self, character: Character) -> bool:
        return True

    def is_completed(self) -> bool:
        return False

    def process_next_state(self, game: Game):
        game.widgets.append(VerticalEffect(ShoppingCart(game.player)))

    def save_state(self) -> dict[str, Any]:
        return {}

    def restore_state(self, state: dict[str, Any]):
        pass

from typing import Any, Protocol

import pyray as pr

from tinyrpg.engine import (
    Character,
    DialogEffect,
    Particle,
    Timer,
    VerticalEffect,
    Widget,
    get_database,
    get_inventory_item,
)
from tinyrpg.particles import PickUp
from tinyrpg.widgets import MessageBox


class Game(Protocol):
    player: Character
    particles: list[Particle] = []
    widgets: list[Widget] = []
    should_end_timer: Timer


class GraceQuest:
    def __init__(self):
        self.quest_name = "Grace's Quest"
        self.quest_description = "Help Grace find her lost gem."
        self.quest_state = 0

    def reset(self):
        self.quest_state = 0

    def is_assignable(self, character: Character) -> bool:
        return True

    def is_completed(self) -> bool:
        return self.quest_state == 3

    def provide_equipment(self, game: Game):
        sword = get_inventory_item("Sword")
        game.particles.append(PickUp(game.player.pos, pr.Vector2(0.25, -1), sword, game.player))
        shield = get_inventory_item("Shield")
        game.particles.append(PickUp(game.player.pos, pr.Vector2(-0.25, -1), shield, game.player))
        self.quest_state = 1

    def give_gem(self, game: Game):
        assert game.player.inventory is not None, "Inventory must exist"
        gem = get_inventory_item("Grace_Gem")
        game.player.inventory.remove(gem)
        # game.particles.append(PickUp(game.player.pos, pr.Vector2(0, -1), gem, game.player))
        self.quest_state = 2

    def provide_reward(self, game: Game):
        assert game.player.inventory is not None, "Inventory must exist"
        potion = get_inventory_item("Potion")
        game.particles.append(PickUp(game.player.pos, pr.Vector2(0, -1), potion, game.player))
        game.should_end_timer.set()
        self.quest_state = 3

    def process_next_state(self, game: Game):
        assert game.player.inventory is not None, "Inventory must exist"
        should_return = False
        while not should_return:
            match self.quest_state:
                case 0:
                    messages: list[list[str]] = get_database().select_dict("messages")["quest_grace"]["1"]
                    game.widgets.append(
                        VerticalEffect(DialogEffect([MessageBox(*m) for m in messages])).on_close(
                            lambda: self.provide_equipment(game)
                        )
                    )
                    should_return = True

                case 1:
                    if game.player.inventory.contains(get_inventory_item("Grace_Gem")):
                        self.give_gem(game)
                    else:
                        messages: list[list[str]] = get_database().select_dict("messages")["quest_grace"]["2"]
                        game.widgets.append(VerticalEffect(DialogEffect([MessageBox(*m) for m in messages])))
                        should_return = True

                case 2:
                    messages: list[list[str]] = get_database().select_dict("messages")["quest_grace"]["3"]
                    game.widgets.append(
                        VerticalEffect(DialogEffect([MessageBox(*m) for m in messages])).on_close(
                            lambda: self.provide_reward(game)
                        )
                    )
                    should_return = True

    def save_state(self) -> dict[str, Any]:
        return {}

    def restore_state(self, state: dict[str, Any]):
        pass

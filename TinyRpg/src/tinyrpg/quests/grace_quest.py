import pyray as pr

from tinyrpg.engine import DialogEffect, Item, VerticalEffect, get_database
from tinyrpg.particles import PickUp
from tinyrpg.widgets import MessageBox, ShoppingCart


class GraceQuest:
    def __init__(self):
        self.quest_name = "Grace's Quest"
        self.quest_description = "Help Grace find her lost gem."
        self.quest_state = 0
        self.gem_to_collect = Item(*get_database().select_dict("items")["Grace_Gem"])

    def is_quest_completed(self) -> bool:
        return self.quest_state == 3

    def provide_equipment(self, game):
        self.quest_state = 1
        sword = Item(*get_database().select_dict("items")["Sword"])
        game.particles.append(PickUp(game.player.pos, pr.Vector2(0.25, -1), sword, game.player))
        shield = Item(*get_database().select_dict("items")["Shield"])
        game.particles.append(PickUp(game.player.pos, pr.Vector2(-0.25, -1), shield, game.player))

    def collect_gem(self) -> Item:
        self.quest_state = 2
        return self.gem_to_collect

    def provide_reward(self, game):
        self.quest_state = 3
        game.player.inventory.drop(game.player.inventory.index(self.gem_to_collect))
        potion = Item(*get_database().select_dict("items")["Potion"])
        game.particles.append(PickUp(game.player.pos, pr.Vector2(0, -1), potion, game.player))

    def process_next_state(self, game):
        match self.quest_state:
            case 0:
                messages: list[list[str]] = get_database().select_dict("messages")["quest_grace"]["1"]
                game.widgets.append(
                    VerticalEffect(DialogEffect([MessageBox(*m) for m in messages])).on_close(
                        lambda: self.provide_equipment(game)
                    )
                )

            case 1:
                messages: list[list[str]] = get_database().select_dict("messages")["quest_grace"]["2"]
                game.widgets.append(VerticalEffect(DialogEffect([MessageBox(*m) for m in messages])))

            case 2:
                messages: list[list[str]] = get_database().select_dict("messages")["quest_grace"]["3"]
                game.widgets.append(
                    VerticalEffect(DialogEffect([MessageBox(*m) for m in messages])).on_close(
                        lambda: self.provide_reward(game)
                    )
                )

            case 3:
                game.widgets.append(VerticalEffect(ShoppingCart(game.player)))

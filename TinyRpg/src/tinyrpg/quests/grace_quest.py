from typing import Optional

import pyray as pr

from tinyrpg.engine import DialogEffect, Item, VerticalEffect
from tinyrpg.items import ITEM_DATABASE
from tinyrpg.messages import (
    MESSAGE_GRACE1,
    MESSAGE_GRACE2,
    MESSAGE_GRACE3,
    MESSAGE_PLAYER1,
    MESSAGE_PLAYER2,
    MESSAGE_PLAYER3,
)
from tinyrpg.particles import PickUp
from tinyrpg.widgets import MessageBox, ShoppingCart


class GraceQuest:
    def __init__(self):
        self.quest_name = "Grace's Quest"
        self.quest_description = "Help Grace find her lost gem."
        self.quest_state = 0
        self.gem_to_collect: Optional[Item] = None

    def is_quest_completed(self) -> bool:
        return self.quest_state == 3

    def collect_gem(self) -> Item:
        self.gem_to_collect = Item(*ITEM_DATABASE[3])
        self.quest_state = 2
        return self.gem_to_collect

    def process_next_state(self, game):
        match self.quest_state:
            case 0:

                def provide_equipment(game=game):
                    self.quest_state = 1
                    game.particles.append(
                        PickUp(game.hero.pos, pr.Vector2(0.25, -1), Item(*ITEM_DATABASE[0]), game.hero)
                    )
                    game.particles.append(
                        PickUp(game.hero.pos, pr.Vector2(-0.25, -1), Item(*ITEM_DATABASE[1]), game.hero)
                    )

                game.widgets.append(
                    DialogEffect(
                        [
                            VerticalEffect(MessageBox("Grace", "portrait-grace", MESSAGE_GRACE1)),
                            VerticalEffect(MessageBox("Romuald", "portrait-player", MESSAGE_PLAYER1)),
                        ]
                    ).on_close(provide_equipment)
                )

            case 1:
                game.widgets.append(
                    DialogEffect(
                        [
                            VerticalEffect(MessageBox("Grace", "portrait-grace", MESSAGE_GRACE2)),
                            VerticalEffect(MessageBox("Romuald", "portrait-player", MESSAGE_PLAYER2)),
                        ]
                    )
                )

            case 2:

                def provide_reward(game=game):
                    assert self.gem_to_collect is not None
                    self.quest_state = 3
                    game.hero.inventory.drop(game.hero.inventory.index(self.gem_to_collect))
                    game.particles.append(PickUp(game.hero.pos, pr.Vector2(0, -1), Item(*ITEM_DATABASE[2]), game.hero))

                game.widgets.append(
                    DialogEffect(
                        [
                            VerticalEffect(MessageBox("Grace", "portrait-grace", MESSAGE_GRACE3)),
                            VerticalEffect(MessageBox("Romuald", "portrait-player", MESSAGE_PLAYER3)),
                        ]
                    ).on_close(provide_reward)
                )

            case 3:
                game.widgets.append(VerticalEffect(ShoppingCart()))

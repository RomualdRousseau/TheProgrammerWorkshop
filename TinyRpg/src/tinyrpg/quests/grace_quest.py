from typing import Optional

import pyray as pr

from tinyrpg.engine import DialogEffect, Item, VerticalEffect
from tinyrpg.items import ITEM_DATABASE
from tinyrpg.messages import (
    MESSAGE_QUEST_GRACE_1_1,
    MESSAGE_QUEST_GRACE_1_2,
    MESSAGE_QUEST_GRACE_1_3,
    MESSAGE_QUEST_GRACE_1_4,
    MESSAGE_QUEST_GRACE_1_5,
    MESSAGE_QUEST_GRACE_1_6,
    MESSAGE_QUEST_GRACE_2_1,
    MESSAGE_QUEST_GRACE_2_2,
    MESSAGE_QUEST_GRACE_2_3,
    MESSAGE_QUEST_GRACE_2_4,
    MESSAGE_QUEST_GRACE_2_5,
    MESSAGE_QUEST_GRACE_2_6,
    MESSAGE_QUEST_GRACE_2_7,
    MESSAGE_QUEST_GRACE_3_1,
    MESSAGE_QUEST_GRACE_3_2,
    MESSAGE_QUEST_GRACE_3_3,
    MESSAGE_QUEST_GRACE_3_4,
    MESSAGE_QUEST_GRACE_3_5,
    MESSAGE_QUEST_GRACE_3_6,
    MESSAGE_QUEST_GRACE_3_7,
    MESSAGE_QUEST_GRACE_3_8,
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

    def provide_equipment(self, game):
        self.quest_state = 1
        game.particles.append(PickUp(game.hero.pos, pr.Vector2(0.25, -1), Item(*ITEM_DATABASE[0]), game.hero))
        game.particles.append(PickUp(game.hero.pos, pr.Vector2(-0.25, -1), Item(*ITEM_DATABASE[1]), game.hero))

    def collect_gem(self) -> Item:
        self.quest_state = 2
        self.gem_to_collect = Item(*ITEM_DATABASE[3])
        return self.gem_to_collect

    def provide_reward(self, game):
        assert self.gem_to_collect is not None
        self.quest_state = 3
        game.hero.inventory.drop(game.hero.inventory.index(self.gem_to_collect))
        game.particles.append(PickUp(game.hero.pos, pr.Vector2(0, -1), Item(*ITEM_DATABASE[2]), game.hero))

    def process_next_state(self, game):
        match self.quest_state:
            case 0:
                game.widgets.append(
                    VerticalEffect(
                        DialogEffect(
                            [
                                MessageBox("Grace", "portrait-grace", MESSAGE_QUEST_GRACE_1_1),
                                MessageBox("Romuald", "portrait-player", MESSAGE_QUEST_GRACE_1_2),
                                MessageBox("Grace", "portrait-grace", MESSAGE_QUEST_GRACE_1_3),
                                MessageBox("Romuald", "portrait-player", MESSAGE_QUEST_GRACE_1_4),
                                MessageBox("Grace", "portrait-grace", MESSAGE_QUEST_GRACE_1_5),
                                MessageBox("Romuald", "portrait-player", MESSAGE_QUEST_GRACE_1_6),
                            ]
                        )
                    ).on_close(lambda: self.provide_equipment(game))
                )

            case 1:
                game.widgets.append(
                    VerticalEffect(
                        DialogEffect(
                            [
                                MessageBox("Grace", "portrait-grace", MESSAGE_QUEST_GRACE_2_1),
                                MessageBox("Romuald", "portrait-player", MESSAGE_QUEST_GRACE_2_2),
                                MessageBox("Grace", "portrait-grace", MESSAGE_QUEST_GRACE_2_3),
                                MessageBox("Romuald", "portrait-player", MESSAGE_QUEST_GRACE_2_4),
                                MessageBox("Grace", "portrait-grace", MESSAGE_QUEST_GRACE_2_5),
                                MessageBox("Romuald", "portrait-player", MESSAGE_QUEST_GRACE_2_6),
                                MessageBox("Grace", "portrait-grace", MESSAGE_QUEST_GRACE_2_7),
                            ]
                        )
                    )
                )

            case 2:
                game.widgets.append(
                    VerticalEffect(
                        DialogEffect(
                            [
                                MessageBox("Grace", "portrait-grace", MESSAGE_QUEST_GRACE_3_1),
                                MessageBox("Romuald", "portrait-player", MESSAGE_QUEST_GRACE_3_2),
                                MessageBox("Grace", "portrait-grace", MESSAGE_QUEST_GRACE_3_3),
                                MessageBox("Romuald", "portrait-player", MESSAGE_QUEST_GRACE_3_4),
                                MessageBox("Grace", "portrait-grace", MESSAGE_QUEST_GRACE_3_5),
                                MessageBox("Romuald", "portrait-player", MESSAGE_QUEST_GRACE_3_6),
                                MessageBox("Grace", "portrait-grace", MESSAGE_QUEST_GRACE_3_7),
                                MessageBox("Romuald", "portrait-player", MESSAGE_QUEST_GRACE_3_8),
                            ]
                        )
                    ).on_close(lambda: self.provide_reward(game))
                )

            case 3:
                game.widgets.append(VerticalEffect(ShoppingCart()))

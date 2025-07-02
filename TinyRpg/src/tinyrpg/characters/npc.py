from typing import Optional

import pyray as pr

from tinyrpg.characters.player import Player
from tinyrpg.characters.rules import Rules
from tinyrpg.engine import CHARACTER_SIZE, Animation, AnimationFlag, Character, CharacterStats, Quest

NPC_ANIMATIONS = lambda: {
    "Idle": Animation(pr.Vector2(0, 0), CHARACTER_SIZE, 6, 3),
    "WalkUp": Animation(pr.Vector2(0, 5), CHARACTER_SIZE, 6, 5),
    "WalkDown": Animation(pr.Vector2(0, 3), CHARACTER_SIZE, 6, 5),
    "WalkLeft": Animation(pr.Vector2(0, 4), CHARACTER_SIZE, 6, 5, AnimationFlag.MIRROR_X),
    "WalkRight": Animation(pr.Vector2(0, 4), CHARACTER_SIZE, 6, 5),
}

NPC_STATS = lambda: CharacterStats(
    speed=8,  # pixel * s-1
    attack_speed=1,  # s
    damage=0,
    armor=0,
    hp=1,
)


class Npc(Character):
    def __init__(self, name: str, pos: pr.Vector2, boundary: pr.BoundingBox, quests: list[Quest]) -> None:
        super().__init__(name, name, pos, NPC_STATS(), NPC_ANIMATIONS(), boundary, Rules())
        self.quests = quests

    def get_next_quest(self, player: Player) -> Optional[Quest]:
        return next((q for q in self.quests if q.is_assignable(player) and not q.is_completed()), None)

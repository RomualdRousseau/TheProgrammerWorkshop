from typing import Optional

import pyray as pr

from tinyrpg.engine.animation import Animation, AnimationFlag
from tinyrpg.engine.character import Character, CharacterStats
from tinyrpg.engine.entity import Entity

NPC_SIZE = pr.Vector2(32, 32)  # pixels
NPC_ANIMATIONS = lambda: {
    "Idle": Animation(pr.Vector2(0, 0), NPC_SIZE, 6, 3),
    "WalkUp": Animation(pr.Vector2(0, 5), NPC_SIZE, 6, 5),
    "WalkDown": Animation(pr.Vector2(0, 3), NPC_SIZE, 6, 5),
    "WalkLeft": Animation(pr.Vector2(0, 4), NPC_SIZE, 6, 5, AnimationFlag.MIRROR_X),
    "WalkRight": Animation(pr.Vector2(0, 4), NPC_SIZE, 6, 5),
}

NPC_SPEED = 8  # pixel * s-1
NPC_ATTACK_SPEED = 1  # frame
NPC_DAMAGE = 1
NPC_ARMOR = 0
NPC_LIFE = 1
NPC_STATS = lambda: CharacterStats(NPC_SPEED, NPC_ATTACK_SPEED, NPC_DAMAGE, NPC_ARMOR, NPC_LIFE)


class Npc(Character):
    def __init__(self, name: str, pos: pr.Vector2) -> None:
        super().__init__(name, pos, NPC_STATS(), NPC_ANIMATIONS())

    def collide(self, dt: float, collision_vector: pr.Vector2, other: Optional[Entity] = None):
        # super().collide(dt, collision_vector, other)
        # self.actions |= CharacterAction.COLLIDING
        # self.events.append(CharacterEvent("collide", other))
        pass

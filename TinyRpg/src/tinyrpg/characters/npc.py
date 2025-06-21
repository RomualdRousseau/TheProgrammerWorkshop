from typing import Optional

import pyray as pr

from tinyrpg.engine import CHARACTER_SIZE, Animation, AnimationFlag, Character, CharacterStats, Entity

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
    def __init__(self, name: str, pos: pr.Vector2, boundary: pr.BoundingBox) -> None:
        super().__init__(name, name, pos, NPC_STATS(), NPC_ANIMATIONS(), boundary)

    def collide(self, dt: float, collision_vector: pr.Vector2, other: Optional[Entity] = None):
        pass

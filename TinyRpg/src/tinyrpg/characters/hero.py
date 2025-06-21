from functools import cache

import pyray as pr

from tinyrpg.constants import INPUT_ATTACK, ITEM_DATABASE
from tinyrpg.engine import (
    CHARACTER_SIZE,
    Animation,
    AnimationFlag,
    Character,
    CharacterAction,
    CharacterStats,
    Item,
    is_key_down,
)

HERO_ANIMATIONS = lambda: {
    "Idle": Animation(pr.Vector2(0, 0), CHARACTER_SIZE, 6, 3),
    "WalkUp": Animation(pr.Vector2(0, 5), CHARACTER_SIZE, 6, 5),
    "WalkDown": Animation(pr.Vector2(0, 3), CHARACTER_SIZE, 6, 5),
    "WalkLeft": Animation(pr.Vector2(0, 4), CHARACTER_SIZE, 6, 5, AnimationFlag.MIRROR_X),
    "WalkRight": Animation(pr.Vector2(0, 4), CHARACTER_SIZE, 6, 5),
    "AttackUp": Animation(pr.Vector2(0, 8), CHARACTER_SIZE, 4, 5),
    "AttackDown": Animation(pr.Vector2(0, 6), CHARACTER_SIZE, 4, 5),
    "AttackLeft": Animation(pr.Vector2(0, 7), CHARACTER_SIZE, 4, 5, AnimationFlag.MIRROR_X),
    "AttackRight": Animation(pr.Vector2(0, 7), CHARACTER_SIZE, 4, 5),
    "Die": Animation(pr.Vector2(0, 9), CHARACTER_SIZE, 4, 5, AnimationFlag.NONE, False),
}

HERO_STATS = lambda: CharacterStats(
    speed=8,  # pixel * s-1
    attack_speed=0.5,  # s
    damage=1,
    armor=1,
    hp=10,
)


class Hero(Character):
    def __init__(self, name: str, pos: pr.Vector2, boundary: pr.BoundingBox) -> None:
        super().__init__("player", name, pos, HERO_STATS(), HERO_ANIMATIONS(), boundary)
        self.inventory.bag[0] = Item(*ITEM_DATABASE[0])
        self.inventory.bag[1] = Item(*ITEM_DATABASE[1])
        self.inventory.bag[2] = Item(*ITEM_DATABASE[2])
        self.inventory.bag[3] = Item(*ITEM_DATABASE[3])

    def handle_ai(self) -> None:
        self.dir = pr.vector2_zero()
        self.speed = 0
        self.actions = CharacterAction.IDLING
        if is_key_down("UP"):
            self.dir.y = -1
            self.actions = CharacterAction.WALKING
            self.speed = self.stats.speed
        elif is_key_down("DOWN"):
            self.dir.y = 1
            self.actions = CharacterAction.WALKING
            self.speed = self.stats.speed
        if is_key_down("LEFT"):
            self.dir.x = -1
            self.actions = CharacterAction.WALKING
            self.speed = self.stats.speed
        elif is_key_down("RIGHT"):
            self.dir.x = 1
            self.actions = CharacterAction.WALKING
            self.speed = self.stats.speed
        if is_key_down(INPUT_ATTACK):
            self.actions = CharacterAction.ATTACKING
            self.speed = 0


@cache
def get_hero() -> Hero:
    return Hero("Romuald", pr.vector2_zero(), pr.BoundingBox((0, 0), (0, 0)))

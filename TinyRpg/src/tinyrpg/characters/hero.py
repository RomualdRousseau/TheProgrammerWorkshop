from functools import cache

import pyray as pr

from tinyrpg.constants import ITEM_DATABASE
from tinyrpg.engine import Animation, AnimationFlag, Character, CharacterAction, CharacterStats
from tinyrpg.engine.inventory import Item

HERO_SIZE = pr.Vector2(32, 32)  # pixels
HERO_ANIMATIONS = lambda: {
    "Idle": Animation(pr.Vector2(0, 0), HERO_SIZE, 6, 3),
    "WalkUp": Animation(pr.Vector2(0, 5), HERO_SIZE, 6, 5),
    "WalkDown": Animation(pr.Vector2(0, 3), HERO_SIZE, 6, 5),
    "WalkLeft": Animation(pr.Vector2(0, 4), HERO_SIZE, 6, 5, AnimationFlag.MIRROR_X),
    "WalkRight": Animation(pr.Vector2(0, 4), HERO_SIZE, 6, 5),
    "AttackUp": Animation(pr.Vector2(0, 8), HERO_SIZE, 4, 5),
    "AttackDown": Animation(pr.Vector2(0, 6), HERO_SIZE, 4, 5),
    "AttackLeft": Animation(pr.Vector2(0, 7), HERO_SIZE, 4, 5, AnimationFlag.MIRROR_X),
    "AttackRight": Animation(pr.Vector2(0, 7), HERO_SIZE, 4, 5),
    "Die": Animation(pr.Vector2(0, 9), HERO_SIZE, 4, 5, AnimationFlag.NONE, False),
}

HERO_SPEED = 16  # pixel * s-1
HERO_ATTACK_SPEED = 0.5  # second
HERO_DAMAGE = 1
HERO_ARMOR = 1
HERO_LIFE = 10
HERO_STATS = lambda: CharacterStats(HERO_SPEED, HERO_ATTACK_SPEED, HERO_DAMAGE, HERO_ARMOR, HERO_LIFE)


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
        if pr.is_key_down(pr.KeyboardKey.KEY_UP):
            self.dir.y = -1
            self.actions = CharacterAction.WALKING
            self.speed = HERO_SPEED
        elif pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
            self.dir.y = 1
            self.actions = CharacterAction.WALKING
            self.speed = HERO_SPEED
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
            self.dir.x = -1
            self.actions = CharacterAction.WALKING
            self.speed = HERO_SPEED
        elif pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
            self.dir.x = 1
            self.actions = CharacterAction.WALKING
            self.speed = HERO_SPEED
        if pr.is_key_down(pr.KeyboardKey.KEY_SPACE):
            self.actions = CharacterAction.ATTACKING
            self.speed = 0


@cache
def get_hero() -> Hero:
    return Hero("Romuald", pr.vector2_zero(), pr.BoundingBox((0, 0), (0, 0)))

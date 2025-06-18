import pyray as pr

from tinyrpg.engine.animation import Animation, AnimationFlag
from tinyrpg.engine.character import Character, CharacterAction, CharacterStats

ENEMY_SIZE = pr.Vector2(32, 32)  # pixels
ENEMY_ANIMATIONS = lambda: {
    "Idle": Animation(pr.Vector2(0, 0), ENEMY_SIZE, 6, 3),
    "WalkUp": Animation(pr.Vector2(0, 5), ENEMY_SIZE, 6, 5),
    "WalkDown": Animation(pr.Vector2(0, 3), ENEMY_SIZE, 6, 5),
    "WalkLeft": Animation(pr.Vector2(0, 4), ENEMY_SIZE, 6, 5, AnimationFlag.MIRROR_X),
    "WalkRight": Animation(pr.Vector2(0, 4), ENEMY_SIZE, 6, 5),
    "AttackUp": Animation(pr.Vector2(0, 9), ENEMY_SIZE, 4, 5),
    "AttackDown": Animation(pr.Vector2(0, 7), ENEMY_SIZE, 4, 5),
    "AttackLeft": Animation(pr.Vector2(0, 8), ENEMY_SIZE, 4, 5, AnimationFlag.MIRROR_X),
    "AttackRight": Animation(pr.Vector2(0, 8), ENEMY_SIZE, 4, 5),
    "Die": Animation(pr.Vector2(0, 6), ENEMY_SIZE, 4, 5, AnimationFlag.NONE, False),
}

ENEMY_SPEED = 8  # pixel * s-1
ENEMY_ATTACK_SPEED = 0.8  # s
ENEMY_DAMAGE = 1
ENEMY_ARMOR = 0
ENEMY_LIFE = 2
ENEMY_STATS = lambda: CharacterStats(ENEMY_SPEED, ENEMY_ATTACK_SPEED, ENEMY_DAMAGE, ENEMY_ARMOR, ENEMY_LIFE)


class Enemy(Character):
    def __init__(self, name: str, pos: pr.Vector2) -> None:
        super().__init__(
            name,
            pos,
            ENEMY_STATS(),
            ENEMY_ANIMATIONS(),
        )
        print(self.stats)

    def handle_ai(self):
        if self.trigger_near.curr is not None:
            self.dir = pr.vector2_normalize(pr.vector2_subtract(self.trigger_near.curr.pos, self.pos))
            self.speed = 0
            self.actions = CharacterAction.ATTACKING
        elif self.trigger_far.curr is not None:
            self.dir = pr.vector2_normalize(pr.vector2_subtract(self.trigger_far.curr.pos, self.pos))
            self.speed = ENEMY_SPEED
            self.actions = CharacterAction.WALKING
        else:
            self.dir = pr.vector2_zero()
            self.speed = 0
            self.actions = CharacterAction.IDLING

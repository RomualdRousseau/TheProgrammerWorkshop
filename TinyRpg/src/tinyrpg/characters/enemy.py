import pyray as pr

from tinyrpg import rules
from tinyrpg.engine import CHARACTER_SIZE, Animation, AnimationFlag, Character, CharacterAction, CharacterStats
from tinyrpg.engine.game.character import CHARACTER_NO_RESET_MASK

ENEMY_ANIMATIONS = lambda: {
    "Idle": Animation(pr.Vector2(0, 0), CHARACTER_SIZE, 6, 3),
    "WalkUp": Animation(pr.Vector2(0, 5), CHARACTER_SIZE, 6, 5),
    "WalkDown": Animation(pr.Vector2(0, 3), CHARACTER_SIZE, 6, 5),
    "WalkLeft": Animation(pr.Vector2(0, 4), CHARACTER_SIZE, 6, 5, AnimationFlag.MIRROR_X),
    "WalkRight": Animation(pr.Vector2(0, 4), CHARACTER_SIZE, 6, 5),
    "AttackUp": Animation(pr.Vector2(0, 9), CHARACTER_SIZE, 4, 5),
    "AttackDown": Animation(pr.Vector2(0, 7), CHARACTER_SIZE, 4, 5),
    "AttackLeft": Animation(pr.Vector2(0, 8), CHARACTER_SIZE, 4, 5, AnimationFlag.MIRROR_X),
    "AttackRight": Animation(pr.Vector2(0, 8), CHARACTER_SIZE, 4, 5),
    "Die": Animation(pr.Vector2(0, 6), CHARACTER_SIZE, 4, 5, AnimationFlag.NONE, False),
}

ENEMY_STATS = lambda: CharacterStats(
    speed=8,  # pixel * s-1
    attack_speed=0.8,  # s
    damage=1,
    armor=0,
    hp=2,
)


class Enemy(Character):
    def __init__(self, name: str, pos: pr.Vector2, boundary: pr.BoundingBox):
        super().__init__(name, name, pos, ENEMY_STATS(), ENEMY_ANIMATIONS(), boundary, rules)

    def handle_ai(self):
        super().handle_ai()
        if self.trigger_near.curr is not None:
            self.dir = pr.vector2_normalize(pr.vector2_subtract(self.trigger_near.curr.pos, self.pos))
            self.speed = 0
            self.actions = (self.actions & CHARACTER_NO_RESET_MASK) | CharacterAction.ATTACKING
        elif self.trigger_far.curr is not None:
            self.dir = pr.vector2_normalize(pr.vector2_subtract(self.trigger_far.curr.pos, self.pos))
            self.speed = self.stats.speed
            self.actions = (self.actions & CHARACTER_NO_RESET_MASK) | CharacterAction.WALKING

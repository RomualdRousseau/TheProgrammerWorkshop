import pyray as pr

from tinyrpg import EPSILON
from tinyrpg.resources import load_resource
from tinyrpg.sprites.animation import Animation
from tinyrpg.sprites.sprite import AnimatedSprite


HERO_WORD_BOUNDARY = pr.Rectangle(-128 - 8, -128 - 8, 256 - 32, 256 - 32)  # pixels
HERO_SPEED = 24  # pixel * s-1
HERO_SIZE = pr.Vector2(48, 48)  # pixels

HERO_ANIMATIONS = {
    "Idle": Animation(pr.Vector2(0, 0), HERO_SIZE, 2, 2),
    "WalkUp": Animation(pr.Vector2(2, 1), HERO_SIZE, 2, 5),
    "WalkDown": Animation(pr.Vector2(2, 0), HERO_SIZE, 2, 5),
    "WalkLeft": Animation(pr.Vector2(2, 2), HERO_SIZE, 2, 5),
    "WalkRight": Animation(pr.Vector2(2, 3), HERO_SIZE, 2, 5),
    "AttackUp": Animation(pr.Vector2(6, 1), HERO_SIZE, 2, 5),
    "AttackDown": Animation(pr.Vector2(6, 0), HERO_SIZE, 2, 5),
    "AttackLeft": Animation(pr.Vector2(6, 2), HERO_SIZE, 2, 5),
    "AttackRight": Animation(pr.Vector2(6, 3), HERO_SIZE, 2, 5),
}


class Hero(AnimatedSprite):
    def __init__(self, pos: pr.Vector2) -> None:
        super().__init__(load_resource("hero"), pos, HERO_ANIMATIONS)
        self.reset()

    def reset(self):
        self.vel = pr.vector2_zero()
        self.dir = pr.vector2_zero()
        self.speed = 0
        self.attack = False

    def input(self) -> None:
        if pr.is_key_down(pr.KeyboardKey.KEY_UP):
            self.dir.y = -1
            self.speed = HERO_SPEED
        elif pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
            self.dir.y = 1
            self.speed = HERO_SPEED
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
            self.dir.x = -1
            self.speed = HERO_SPEED
        elif pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
            self.dir.x = 1
            self.speed = HERO_SPEED
        if pr.is_key_down(pr.KeyboardKey.KEY_SPACE):
            self.attack = True
            self.speed = 0

    def animate(self) -> None:
        if not self.attack:
            if self.dir.x < 0:
                self.set_animation("WalkLeft")
            elif self.dir.x > 0:
                self.set_animation("WalkRight")
            elif self.dir.y < 0:
                self.set_animation("WalkUp")
            elif self.dir.y > 0:
                self.set_animation("WalkDown")
            else:
                self.set_animation("Idle")
        else:
            if self.dir.x < 0:
                self.set_animation("AttackLeft")
            elif self.dir.x > 0:
                self.set_animation("AttackRight")
            elif self.dir.y < 0:
                self.set_animation("AttackUp")
            elif self.dir.y > 0:
                self.set_animation("AttackDown")
            else:
                self.set_animation("AttackDown")

    def update(self, dt: float):
        friction = -self.speed * (dt - 1) / (dt + EPSILON)
        force = pr.vector2_scale(self.dir, self.speed + friction)
        self.reset()
        self.input()
        self.move(force, 1, dt)
        self.constrain_to_world(HERO_WORD_BOUNDARY)
        super().update(dt)

    def draw(self):
        self.animate()
        super().draw()

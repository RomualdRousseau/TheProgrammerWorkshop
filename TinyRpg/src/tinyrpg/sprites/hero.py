import pyray as pr

from tinyrpg.sprites.animation import Animation, AnimationFlag
from tinyrpg.sprites.sprite import AnimatedSprite
from tinyrpg.utils.resources import load_sound, load_texture

HERO_WORD_BOUNDARY = pr.Rectangle(-160 - 8, -160 - 16, 320 - 16, 320 - 16)  # pixels
HERO_SPEED = 16  # pixel * s-1
HERO_SIZE = pr.Vector2(32, 32)  # pixels

HERO_ANIMATIONS = {
    "Idle": Animation(pr.Vector2(0, 0), HERO_SIZE, 6, 3),
    "WalkUp": Animation(pr.Vector2(0, 5), HERO_SIZE, 6, 5),
    "WalkDown": Animation(pr.Vector2(0, 3), HERO_SIZE, 6, 5),
    "WalkLeft": Animation(pr.Vector2(0, 4), HERO_SIZE, 6, 5, AnimationFlag.MIRROR_X),
    "WalkRight": Animation(pr.Vector2(0, 4), HERO_SIZE, 6, 5),
    "AttackUp": Animation(pr.Vector2(0, 8), HERO_SIZE, 4, 5),
    "AttackDown": Animation(pr.Vector2(0, 6), HERO_SIZE, 4, 5),
    "AttackLeft": Animation(pr.Vector2(0, 7), HERO_SIZE, 4, 5, AnimationFlag.MIRROR_X),
    "AttackRight": Animation(pr.Vector2(0, 7), HERO_SIZE, 4, 5),
}


class Hero(AnimatedSprite):
    def __init__(self, pos: pr.Vector2) -> None:
        super().__init__(load_texture("player"), pos, HERO_ANIMATIONS)
        self.dir = pr.vector2_zero()
        self.speed = 0
        self.attacking = False

    def input(self) -> None:
        self.dir = pr.vector2_zero()
        self.speed = 0
        self.attacking = False
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
            self.attacking = True
            self.speed = 0

    def sound_effect(self) -> None:
        match self.attacking:
            case False if (
                self.speed > 0 and int(self.animation.frame) in (1, 4) and not pr.is_sound_playing(load_sound("step"))
            ):
                pr.play_sound(load_sound("step"))
            case True if (
                self.speed == 0 and int(self.animation.frame) in (0, 1) and not pr.is_sound_playing(load_sound("chop"))
            ):
                pr.play_sound(load_sound("chop"))

    def anim_effect(self) -> None:
        match self.attacking:
            case False if self.dir.x < 0:
                self.set_animation("WalkLeft")
            case False if self.dir.x > 0:
                self.set_animation("WalkRight")
            case False if self.dir.y < 0:
                self.set_animation("WalkUp")
            case False if self.dir.y > 0:
                self.set_animation("WalkDown")
            case True if self.dir.x < 0:
                self.set_animation("AttackLeft")
            case True if self.dir.x > 0:
                self.set_animation("AttackRight")
            case True if self.dir.y < 0:
                self.set_animation("AttackUp")
            case True if self.dir.y > 0:
                self.set_animation("AttackDown")
            case True:
                self.set_animation("AttackDown")
            case _:
                self.set_animation("Idle")

    def update(self, dt: float):
        self.input()
        self.move_constant(pr.vector2_scale(self.dir, self.speed), dt)
        self.constrain_to_world(HERO_WORD_BOUNDARY)
        super().update(dt)

    def draw(self):
        self.sound_effect()
        self.anim_effect()
        super().draw()

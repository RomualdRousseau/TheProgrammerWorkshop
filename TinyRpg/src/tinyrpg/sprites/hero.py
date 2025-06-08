from enum import Flag, auto

import pyray as pr

from tinyrpg.engine.animation import Animation, AnimationFlag
from tinyrpg.engine.sprite import AnimatedSprite
from tinyrpg.resources import load_sound, load_texture

HERO_WORLD_BOUNDARY = pr.BoundingBox((-160 - 8, -160 - 16), (160 - 24, 160 - 24))  # pixels
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


class ActionSprite(Flag):
    IDLING = auto()
    WALKING = auto()
    ATTACKING = auto()
    COLLIDING = auto()
    TALKING = auto()


class Hero(AnimatedSprite):
    def __init__(self, pos: pr.Vector2) -> None:
        super().__init__(load_texture("player"), pos, HERO_ANIMATIONS)
        self.dir = pr.vector2_zero()
        self.speed = 0
        self.action = ActionSprite.IDLING

    def get_layer(self):
        return 1

    def get_depth(self):
        dest = self.animation.get_dest(self.pos.x, self.pos.y)
        return dest.y + dest.height * 0.8

    def start_talk(self):
        self.dir = pr.vector2_zero()
        self.speed = 0
        self.action = ActionSprite.TALKING

    def stop_talk(self):
        self.action = ActionSprite.IDLING

    def handle_input(self) -> None:
        self.dir = pr.vector2_zero()
        self.speed = 0
        self.action = ActionSprite.IDLING
        if pr.is_key_down(pr.KeyboardKey.KEY_UP):
            self.dir.y = -1
            self.action = ActionSprite.WALKING
            self.speed = HERO_SPEED
        elif pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
            self.dir.y = 1
            self.action = ActionSprite.WALKING
            self.speed = HERO_SPEED
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
            self.dir.x = -1
            self.action = ActionSprite.WALKING
            self.speed = HERO_SPEED
        elif pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
            self.dir.x = 1
            self.action = ActionSprite.WALKING
            self.speed = HERO_SPEED
        if pr.is_key_down(pr.KeyboardKey.KEY_SPACE):
            self.action = ActionSprite.ATTACKING
            self.speed = 0

    def play_sound_effect(self) -> None:
        match self.action:
            case ActionSprite.WALKING if int(self.animation.frame) in (1, 4):
                if not pr.is_sound_playing(load_sound("step")):
                    pr.play_sound(load_sound("step"))
            case ActionSprite.ATTACKING if int(self.animation.frame) in (0, 1):
                if not pr.is_sound_playing(load_sound("chop")):
                    pr.play_sound(load_sound("chop"))

    def set_animation_effect(self) -> None:
        match self.action:
            case a if ActionSprite.WALKING in a and self.dir.x < 0:
                self.set_animation("WalkLeft")
            case a if ActionSprite.WALKING in a and self.dir.x > 0:
                self.set_animation("WalkRight")
            case a if ActionSprite.WALKING in a and self.dir.y < 0:
                self.set_animation("WalkUp")
            case a if ActionSprite.WALKING in a and self.dir.y > 0:
                self.set_animation("WalkDown")
            case ActionSprite.ATTACKING if self.dir.x < 0:
                self.set_animation("AttackLeft")
            case ActionSprite.ATTACKING if self.dir.x > 0:
                self.set_animation("AttackRight")
            case ActionSprite.ATTACKING if self.dir.y < 0:
                self.set_animation("AttackUp")
            case ActionSprite.ATTACKING if self.dir.y > 0:
                self.set_animation("AttackDown")
            case ActionSprite.ATTACKING:
                self.set_animation("AttackDown")
            case _:
                self.set_animation("Idle")

    def collide(self, collision_vector: pr.Vector2, dt: float):
        self.action |= ActionSprite.COLLIDING
        super().collide(collision_vector, dt)

    def update(self, dt: float):
        if self.action != ActionSprite.TALKING:
            self.handle_input()
        self.move_constant(pr.vector2_scale(self.dir, self.speed), dt)
        self.constrain_to_world(HERO_WORLD_BOUNDARY)
        super().update(dt)

    def draw(self):
        self.play_sound_effect()
        self.set_animation_effect()
        super().draw()

from enum import Flag, auto

import pyray as pr

from tinyrpg.engine.animation import Animation, AnimationFlag
from tinyrpg.engine.sprite import AnimatedSprite
from tinyrpg.resources import load_sound, load_texture
from tinyrpg.utils.bbox import get_bbox_from_rect

ENEMY_WORLD_BOUNDARY = pr.BoundingBox((-160 - 8, -160 - 16), (160 - 24, 160 - 24))  # pixels
ENEMY_SPEED = 16  # pixel * s-1
ENEMY_SIZE = pr.Vector2(32, 32)  # pixels

ENEMY_ANIMATIONS = {
    "Idle": Animation(pr.Vector2(0, 0), ENEMY_SIZE, 6, 3),
    "WalkUp": Animation(pr.Vector2(0, 5), ENEMY_SIZE, 6, 5),
    "WalkDown": Animation(pr.Vector2(0, 3), ENEMY_SIZE, 6, 5),
    "WalkLeft": Animation(pr.Vector2(0, 4), ENEMY_SIZE, 6, 5, AnimationFlag.MIRROR_X),
    "WalkRight": Animation(pr.Vector2(0, 4), ENEMY_SIZE, 6, 5),
    "AttackUp": Animation(pr.Vector2(0, 8), ENEMY_SIZE, 4, 5),
    "AttackDown": Animation(pr.Vector2(0, 6), ENEMY_SIZE, 4, 5),
    "AttackLeft": Animation(pr.Vector2(0, 7), ENEMY_SIZE, 4, 5, AnimationFlag.MIRROR_X),
    "AttackRight": Animation(pr.Vector2(0, 7), ENEMY_SIZE, 4, 5),
}


class ActionEnemy(Flag):
    IDLING = auto()
    WALKING = auto()
    ATTACKING = auto()
    COLLIDING = auto()
    TALKING = auto()


class Enemy(AnimatedSprite):
    def __init__(self, name: str, pos: pr.Vector2) -> None:
        super().__init__(
            load_texture(name),
            pos,
            ENEMY_ANIMATIONS,
        )
        self.dir = pr.vector2_zero()
        self.speed = 0
        self.action = ActionEnemy.IDLING

    def get_layer(self):
        return 1

    def get_depth(self):
        dest = self.get_dest(self.pos.x, self.pos.y)
        return dest.y + dest.height * 0.8

    def get_bbox(self) -> pr.BoundingBox:
        bbox = get_bbox_from_rect(self.get_dest(self.pos.x, self.pos.y))
        bbox.min = pr.Vector3(bbox.min.x + 12, bbox.min.y + 20, 0)
        bbox.max = pr.Vector3(bbox.max.x - 12, bbox.max.y - 8, 0)
        return bbox

    def start_talk(self):
        self.dir = pr.vector2_zero()
        self.speed = 0
        self.action = ActionEnemy.TALKING

    def stop_talk(self):
        self.action = ActionEnemy.IDLING

    def play_sound_effect(self) -> None:
        match self.action:
            case ActionEnemy.WALKING if int(self.animation.frame) in (1, 4):
                if not pr.is_sound_playing(load_sound("step")):
                    pr.play_sound(load_sound("step"))
            case ActionEnemy.ATTACKING if int(self.animation.frame) in (0, 1):
                if not pr.is_sound_playing(load_sound("hurt")):
                    pr.play_sound(load_sound("hurt"))

    def set_animation_effect(self) -> None:
        match self.action:
            case a if ActionEnemy.WALKING in a and self.dir.x < 0:
                self.set_animation("WalkLeft")
            case a if ActionEnemy.WALKING in a and self.dir.x > 0:
                self.set_animation("WalkRight")
            case a if ActionEnemy.WALKING in a and self.dir.y < 0:
                self.set_animation("WalkUp")
            case a if ActionEnemy.WALKING in a and self.dir.y > 0:
                self.set_animation("WalkDown")
            case ActionEnemy.ATTACKING if self.dir.x < 0:
                self.set_animation("AttackLeft")
            case ActionEnemy.ATTACKING if self.dir.x > 0:
                self.set_animation("AttackRight")
            case ActionEnemy.ATTACKING if self.dir.y < 0:
                self.set_animation("AttackUp")
            case ActionEnemy.ATTACKING if self.dir.y > 0:
                self.set_animation("AttackDown")
            case ActionEnemy.ATTACKING:
                self.set_animation("AttackDown")
            case _:
                self.set_animation("Idle")

    def collide(self, collision_vector: pr.Vector2, dt: float):
        self.action |= ActionEnemy.COLLIDING
        super().collide(collision_vector, dt)

    def update(self, dt: float):
        self.move_constant(pr.vector2_scale(self.dir, self.speed), dt)
        self.constrain_to_world(ENEMY_WORLD_BOUNDARY)
        super().update(dt)

    def draw(self):
        self.play_sound_effect()
        self.set_animation_effect()
        super().draw()

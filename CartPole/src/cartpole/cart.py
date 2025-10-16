import pyray as pr

from cartpole.config import (
    CAMERA_ZOOM,
    CART_MASS,
    CART_MOTOR_POWER,
    CART_OFFSET,
    CART_SIZE,
    EDGE_K,
    GROUND_DRAG,
    WINDOW_WIDTH,
)
from cartpole.game.animation import Animation
from cartpole.game.sprite import Sprite
from cartpole.physic.forces import edge_force, friction_force, motor_force
from cartpole.physic.rigid_body import RigidBody

BOARD_WIDTH = WINDOW_WIDTH / CAMERA_ZOOM

CART_ANIMATIONS = {
    "IDLE": Animation(pr.Vector2(0, 0), pr.Vector2(64, 64), 2, 1),
    "WALK_RIGHT": Animation(pr.Vector2(0, 0), pr.Vector2(64, 64), 3, 5),
    "WALK_LEFT": Animation(pr.Vector2(0, 0), pr.Vector2(64, 64), 3, 5, mirror_x=True),
}


class Cart(RigidBody):
    def __init__(self, pos: pr.Vector2) -> None:
        self.body = RigidBody(CART_MASS, pos)
        self.sprite = Sprite(pr.load_texture("./assets/textures/acrobat.png"), CART_ANIMATIONS)

    def update(self, dt: float) -> None:
        self.body.apply_force(motor_force(CART_MOTOR_POWER))
        self.body.apply_force(friction_force(self.body, GROUND_DRAG))
        self.body.apply_force(
            edge_force(self.body, pr.Vector2(BOARD_WIDTH, self.body.pos.y), CART_SIZE[0] * 0.5, EDGE_K)
        )
        self.body.apply_force(
            edge_force(
                self.body, pr.Vector2(-(BOARD_WIDTH + CART_OFFSET[0]), self.body.pos.y), CART_SIZE[0] * 0.5, EDGE_K
            )
        )
        self.body.update(dt)

        if self.body.vel.x < -0.1:
            self.sprite.set_animation("WALK_LEFT")
        elif self.body.vel.x > 0.1:
            self.sprite.set_animation("WALK_RIGHT")
        else:
            self.sprite.set_animation("IDLE")
        self.sprite.update(dt)

    def draw(self) -> None:
        pos = pr.vector2_subtract(self.body.pos, pr.vector2_scale(CART_SIZE, 0.5))
        self.sprite.draw(pr.Rectangle(pos.x + CART_OFFSET[0], pos.y + CART_OFFSET[1], *CART_SIZE))

import pyray as pr

from tinyrpg.resources import load_resource
from tinyrpg.sprites.animation import Animation
from tinyrpg.sprites.sprite import AnimatedSprite


HERO_SPEED = 24  # pixel * s-1

Idle = Animation(pr.Vector2(0, 0), pr.Vector2(48, 48), 2, 2)
WalkUp = Animation(pr.Vector2(2, 1), pr.Vector2(48, 48), 2, 5)
WalkDown = Animation(pr.Vector2(2, 0), pr.Vector2(48, 48), 2, 5)
WalkLeft = Animation(pr.Vector2(2, 2), pr.Vector2(48, 48), 2, 5)
WalkRight = Animation(pr.Vector2(2, 3), pr.Vector2(48, 48), 2, 5)


class Hero(AnimatedSprite):
    def __init__(self, pos: pr.Vector2) -> None:
        super().__init__(load_resource("hero"), pos, Idle)
        self.dir = pr.vector2_zero()

    def input(self):
        self.dir = pr.vector2_zero()
        if pr.is_key_down(pr.KeyboardKey.KEY_UP):
            self.dir.y = -1
        elif pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
            self.dir.y = 1
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
            self.dir.x = -1
        elif pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
            self.dir.x = 1

    def animate(self):
        if self.dir.x < 0:
            self.set_animation(WalkLeft)
        elif self.dir.x > 0:
            self.set_animation(WalkRight)
        elif self.dir.y < 0:
            self.set_animation(WalkUp)
        elif self.dir.y > 0:
            self.set_animation(WalkDown)
        else:
            self.set_animation(Idle)

    def constrain_to_screen(self):
        self.pos.x = max(-128 - 16, min(self.pos.x, 128 - 32))
        self.pos.y = max(-128 - 16, min(self.pos.y, 128 - 32))

    def update(self, dt: float):
        self.input()
        self.move(self.dir, HERO_SPEED, dt)
        self.constrain_to_screen()
        super().update(dt)

    def draw(self):
        self.animate()
        super().draw()

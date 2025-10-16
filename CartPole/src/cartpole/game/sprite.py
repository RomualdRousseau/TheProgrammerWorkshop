import pyray as pr

from cartpole.game.animation import Animation


class Sprite:
    def __init__(
        self,
        texture: pr.Texture,
        animations: dict[str, Animation],
    ) -> None:
        self.texture = texture
        self.animations = animations
        self.animation = animations["IDLE"]

    def set_animation(self, name: str) -> None:
        new_animation = self.animations[name]
        if new_animation != self.animation:
            self.animation = new_animation
            self.animation.frame = 0

    def update(self, dt: float) -> None:
        self.animation.update(dt)

    def draw(self, dest: pr.Rectangle) -> None:
        pr.draw_texture_pro(
            self.texture,
            self.animation.get_source(),
            dest,
            (0, 0),
            0,
            pr.WHITE,
        )

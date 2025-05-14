import pyray as pr


from tinyrpg.sprites.animation import Animation


class Sprite:
    def __init__(self, texture: pr.Texture, pos: pr.Vector2) -> None:
        self.texture = texture
        self.pos = pos
        self.vel = pr.vector2_zero()

    def move(self, dir: pr.Vector2, speed: float, dt: float) -> None:
        self.vel = pr.vector2_scale(pr.vector2_normalize(dir), speed)
        self.pos = pr.vector2_add(self.pos, pr.vector2_scale(self.vel, dt))

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        pr.draw_texture_v(self.texture, self.pos, pr.WHITE)


class AnimatedSprite(Sprite):
    def __init__(
        self, texture: pr.Texture, pos: pr.Vector2, animation: Animation
    ) -> None:
        super().__init__(texture, pos)
        self.animation = animation

    def set_animation(self, animation: Animation) -> None:
        self.animation = animation

    def update(self, dt: float) -> None:
        super().update(dt)
        self.animation.update(dt)

    def draw(self) -> None:
        pr.draw_texture_pro(
            self.texture,
            self.animation.get_source(),
            self.animation.get_dest(self.pos.x, self.pos.y),
            self.animation.get_origin(),
            0,
            pr.WHITE,
        )

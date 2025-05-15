import pyray as pr


from tinyrpg.sprites.animation import Animation


class Sprite:
    def __init__(self, texture: pr.Texture, pos: pr.Vector2) -> None:
        self.texture = texture
        self.pos = pos
        self.vel = pr.vector2_zero()

    def move(self, force: pr.Vector2, mass: float, dt: float) -> None:
        acc = pr.vector2_scale(force, 1 / mass)
        self.vel = pr.vector2_add(self.vel, pr.vector2_scale(acc, dt))
        self.pos = pr.vector2_add(self.pos, pr.vector2_scale(self.vel, dt))

    def constrain_to_world(self, boundary: pr.Rectangle):
        self.pos.x = max(boundary.x, min(self.pos.x, boundary.x + boundary.width))
        self.pos.y = max(boundary.y, min(self.pos.y, boundary.y + boundary.height))

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        pr.draw_texture_v(self.texture, self.pos, pr.WHITE)


class AnimatedSprite(Sprite):
    def __init__(
        self,
        texture: pr.Texture,
        pos: pr.Vector2,
        animations: dict[str, Animation],
        default_name: str = "Idle",
    ) -> None:
        super().__init__(texture, pos)
        self.animations = animations
        self.animation = animations[default_name]

    def set_animation(self, name: str) -> None:
        new_animation = self.animations[name]
        if self.animation != new_animation:
            self.animation = new_animation
            self.frame = 0

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

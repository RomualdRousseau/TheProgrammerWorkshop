import pyray as pr

from spacerace import PLAYER_MASS, PLAYER_SPEED, WINDOW_HEIGHT
from spacerace.utils.resources import get_sound, get_texture


class Player:
    def __init__(self, x: float, y: float, keys: tuple[int, int]):
        self.x = x
        self.y = y
        self.keys = keys
        self.y_start = y

    def get_collision_box(self) -> tuple[float, float, float, float]:
        return (
            self.x - PLAYER_MASS * 0.5,
            self.y - PLAYER_MASS * 0.5,
            PLAYER_MASS * 2 * 0.5,
            PLAYER_MASS * 2 * 0.5,
        )

    def reset(self):
        self.y = self.y_start

    def update(self, dt: float):
        speed = 0.0
        if pr.is_key_down(self.keys[0]):
            speed = -PLAYER_SPEED
        if pr.is_key_down(self.keys[1]):
            speed = PLAYER_SPEED

        self.y = min(max(PLAYER_MASS, self.y + speed * dt), WINDOW_HEIGHT - PLAYER_MASS)

    def draw(self):
        image = get_texture("spaceship")
        scale = image.width / PLAYER_MASS
        pos = pr.Vector2(self.x - PLAYER_MASS * scale, self.y - PLAYER_MASS * scale)
        pr.draw_texture_ex(image, pos, 0, scale, pr.WHITE)
        # pr.draw_rectangle_rec(self.get_collision_box(), pr.BLUE)

    def collide(self):
        pr.play_sound(get_sound("explosion"))
        self.reset()

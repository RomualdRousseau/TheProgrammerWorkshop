import pyray as pr

from tinyrpg.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from tinyrpg.engine.particle import Particle
from tinyrpg.engine.renderer import renderer_unsorted_draw

MESSAGE_HEIGHT = 200  # pixels
MESSAGE_BORDER = 20  # pixels
MESSAGE_FONT_SIZE = 40  # pixels
MESSAGE_FADE_SPEED = 4  # pixels.s-1


class Message(Particle):
    def __init__(self, greeting: str, camera: pr.Camera2D):
        super().__init__(pr.Vector2(MESSAGE_BORDER, WINDOW_HEIGHT - MESSAGE_HEIGHT - MESSAGE_BORDER))
        self.greeting = greeting
        self.camera = camera
        self.state = 0
        self.fade_time = 0

    def handle_input(self):
        if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
            self.state = 2

    def update(self, dt: float):
        match self.state:
            case 0:
                self.life = 100
                self.fade_time += MESSAGE_FADE_SPEED * dt
                if self.fade_time >= 1:
                    self.fade_time = 1
                    self.state = 1
            case 1:
                self.life = 100
                self.handle_input()
            case 2:
                self.life = 100
                self.fade_time -= MESSAGE_FADE_SPEED * dt
                if self.fade_time <= 0:
                    self.life = 0
                    self.state = 3
        super().update(dt)

    @renderer_unsorted_draw
    def draw(self):
        pos = pr.get_screen_to_world_2d(self.pos, self.camera)
        size = pr.Vector2((WINDOW_WIDTH - MESSAGE_BORDER * 2) / self.camera.zoom, MESSAGE_HEIGHT / self.camera.zoom)
        off_y, size_y = size.y * (1 - self.fade_time) // 2, size.y * self.fade_time
        rect = pr.Rectangle(pos.x, pos.y + off_y, size.x, size_y)
        pr.draw_rectangle_rec(rect, pr.color_alpha(pr.BLUE, 0.8))
        pr.draw_rectangle_lines_ex(rect, 1, pr.RAYWHITE)
        if self.state == 1:
            font_size = int(MESSAGE_FONT_SIZE / self.camera.zoom)
            pr.draw_text(self.greeting, int(pos.x + 2), int(pos.y + 2), font_size, pr.RAYWHITE)

import pyray as pr

from tinyrpg.engine import Scene


class FadeInOut:
    def __init__(self, state: str, previous_scene: Scene, next_scene: Scene):
        self.state = state
        self.previous_scene = previous_scene
        self.next_scene = next_scene

    def init(self):
        self.time = 0

        self.previous_scene.draw()
        image = pr.load_image_from_screen()
        self.texture = pr.load_texture_from_image(image)
        pr.unload_image(image)
        self.previous_scene.release()

        self.next_scene.init()

    def release(self):
        pass

    def update(self, dt: float):
        self.time += dt

    def draw(self):
        if self.next_scene:
            self.next_scene.draw()
        if self.texture:
            pr.draw_texture(self.texture, 0, 0, pr.color_alpha(pr.WHITE, 1.0 - min(self.time, 1.0)))

    def get_state_and_input(self) -> tuple[str, str]:
        if self.time > 1.0:
            return (self.state, "complete")
        else:
            return (self.state, "self")

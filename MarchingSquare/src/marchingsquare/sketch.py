import pyray as pr


def init() -> None:
    pass


def release() -> None:
    pass


def update(dt: float) -> None:
    pass


def draw() -> None:
    pr.clear_background(pr.BLACK)
    pr.draw_text("Hello the world", 10, 10, 20, pr.RAYWHITE)

import pyray as pr

from spacerace import ACTION_KEYPRESS, ACTION_NONE


def init():
    pass


def close():
    pass


def update(dt: float):
    pass


def draw():
    pr.clear_background(pr.BLUE)
    pr.draw_text("Press any key to start", 10, 10, 20, pr.WHITE)


def get_action() -> str:
    return ACTION_KEYPRESS if pr.get_key_pressed() else ACTION_NONE

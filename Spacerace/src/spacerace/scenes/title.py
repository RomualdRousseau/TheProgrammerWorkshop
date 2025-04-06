import pyray as pr

from spacerace import ACTION_KEYPRESS, ACTION_NONE
from spacerace.utils.resources import get_texture


def init():
    pass


def release():
    pass


def update(dt: float):
    pass


def draw():
    pr.clear_background(pr.BLACK)
    pr.draw_texture(get_texture("title"), 0, 0, pr.WHITE)


def get_action() -> str:
    if pr.get_key_pressed():
        return ACTION_KEYPRESS
    else:
        return ACTION_NONE

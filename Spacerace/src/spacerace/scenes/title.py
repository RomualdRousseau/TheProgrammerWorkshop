import pyray as pr

from spacerace import ACTION_KEYPRESS, ACTION_NONE, START_CONTROL
from spacerace.utils.resources import get_texture, release_resources


def init():
    pass


def release():
    release_resources()


def update(dt: float):
    pass


def draw():
    pr.clear_background(pr.BLACK)
    pr.draw_texture(get_texture("title"), 0, 0, pr.WHITE)


def get_action() -> str:
    if pr.is_key_pressed(START_CONTROL):
        return ACTION_KEYPRESS
    else:
        return ACTION_NONE

import pyray as pr

from spacerace import ACTION_KEYPRESS, ACTION_NONE, START_CONTROL


def init():
    pass


def release():
    pass


def update(dt: float):
    pass


def draw():
    pr.clear_background(pr.GREEN)


def get_action() -> str:
    if pr.is_key_pressed(START_CONTROL):
        return ACTION_KEYPRESS
    else:
        return ACTION_NONE


import pyray as pr

from spacerace import (
    ACTION_KEYPRESS,
    ACTION_NONE,
    ACTION_TIMEOUT,
    GAME_OVER_TIMEOUT,
    START_CONTROL,
)


class Context:
    timer: float = 0.0


def init():
   Context.timer = 0.0


def release():
    pass


def update(dt: float):
    Context.timer += dt


def draw():
    pr.clear_background(pr.RED)


def get_action() -> str:
    if Context.timer == 0.0:
        return ACTION_TIMEOUT
    elif Context.timer < GAME_OVER_TIMEOUT // 2 and pr.is_key_pressed(START_CONTROL):
        return ACTION_KEYPRESS
    else:
        return ACTION_NONE

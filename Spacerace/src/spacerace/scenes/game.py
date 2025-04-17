import pyray as pr

from spacerace import ACTION_NONE, ACTION_TIMEOUT, GAME_TIMEOUT


class Context:
    timer: float = 0.0

def init():
    Context.timer = GAME_TIMEOUT


def release():
    pass


def update(dt: float):
    Context.timer = max(0.0, Context.timer - dt)


def draw():
    pr.clear_background(pr.BLUE)
    pr.draw_text(f"{Context.timer:.0f}", 10, 10, 50, pr.RAYWHITE)


def get_action() -> str:
    if Context.timer == 0.0:
        return ACTION_TIMEOUT
    else:
        return ACTION_NONE

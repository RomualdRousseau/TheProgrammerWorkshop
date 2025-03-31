import pyray as pr

from spacerace import ACTION_NONE, ACTION_TIMEOUT


class Context:
    timer_in_s = 0.0


def init():
    pass


def close():
    Context.timer_in_s = 0.0


def update(dt: float):
    Context.timer_in_s += dt


def draw():
    pr.clear_background(pr.BLACK)
    pr.draw_text(f"{Context.timer_in_s:.0f}s", 10, 10, 100, pr.WHITE)


def get_action() -> str:
    return ACTION_TIMEOUT if Context.timer_in_s >= 10 else ACTION_NONE

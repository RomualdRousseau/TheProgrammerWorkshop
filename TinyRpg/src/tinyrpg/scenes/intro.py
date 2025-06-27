import pyray as pr


def init():
    pass


def release():
    pass


def update(dt: float):
    pass


def draw():
    pr.clear_background(pr.BLUE)


def get_state_and_input() -> tuple[str, str]:
    if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
        return ("intro", "keypress")
    else:
        return ("intro", "self")

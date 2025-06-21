import pyray as pr

INPUT_ACTION_MAP = {
    "UP": [pr.KeyboardKey.KEY_UP, pr.KeyboardKey.KEY_W],
    "DOWN": [pr.KeyboardKey.KEY_DOWN, pr.KeyboardKey.KEY_S],
    "LEFT": [pr.KeyboardKey.KEY_LEFT, pr.KeyboardKey.KEY_A],
    "RIGHT": [pr.KeyboardKey.KEY_RIGHT, pr.KeyboardKey.KEY_D],
    "SQUARE": [pr.KeyboardKey.KEY_Z],
    "CROSS": [pr.KeyboardKey.KEY_X],
    "CIRCLE": [pr.KeyboardKey.KEY_C],
    "TRIANGLE": [pr.KeyboardKey.KEY_V],
    "START": [pr.KeyboardKey.KEY_TAB],
    "HOME": [pr.KeyboardKey.KEY_HOME],
}


def is_key_down(key: str) -> bool:
    action_map = INPUT_ACTION_MAP[key]
    return any(pr.is_key_down(x) for x in action_map)


def is_key_pressed(key: str) -> bool:
    action_map = INPUT_ACTION_MAP[key]
    return any(pr.is_key_pressed(x) for x in action_map)

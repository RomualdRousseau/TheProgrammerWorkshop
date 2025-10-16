import pyray as pr

from cartpole import sketch
from cartpole.config import APP_NAME, FRAME_RATE, WINDOW_HEIGHT, WINDOW_WIDTH


def main() -> None:
    pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME)
    pr.set_target_fps(FRAME_RATE)

    state = sketch.init()

    while not pr.window_should_close():
        state = sketch.update(state)
        pr.begin_drawing()
        sketch.draw(state)
        pr.end_drawing()

    sketch.release(state)

    pr.close_window()


if __name__ == "__main__":
    main()

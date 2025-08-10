import pyray as pr

from metaball import sketch
from metaball.constants import APP_NAME, FRAME_RATE, WINDOW_HEIGHT, WINDOW_WIDTH


def main():
    pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME)
    pr.set_target_fps(FRAME_RATE)

    scene = sketch
    scene.init()

    while not pr.window_should_close():
        scene.update(pr.get_frame_time())

        pr.begin_drawing()
        scene.draw()
        pr.end_drawing()

    scene.release()

    pr.close_window()


if __name__ == "__main__":
    main()

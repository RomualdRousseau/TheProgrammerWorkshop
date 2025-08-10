import pyray as pr

from threebody.constants import APP_NAME, FRAME_RATE, WINDOW_HEIGHT, WINDOW_WIDTH
from threebody.scenes import galaxy


def main():
    pr.set_config_flags(pr.ConfigFlags.FLAG_MSAA_4X_HINT)
    pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME)
    pr.set_target_fps(FRAME_RATE)
    pr.hide_cursor()

    scene = galaxy
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

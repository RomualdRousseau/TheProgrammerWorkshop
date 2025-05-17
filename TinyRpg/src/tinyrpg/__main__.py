import pyray as pr

from tinyrpg import APP_NAME, FRAME_RATE, WINDOW_HEIGHT, WINDOW_WIDTH
from tinyrpg.scenes import game


def main():
    pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME)
    pr.set_target_fps(FRAME_RATE)
    pr.init_audio_device()
    
    scene = game
    scene.init()

    while not pr.window_should_close():
        scene.update(pr.get_frame_time())

        pr.begin_drawing()
        scene.draw()
        pr.end_drawing()

    scene.release()

    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()

import pyray as pr

from spacerace import APP_NAME, FRAME_RATE, WINDOW_HEIGHT, WINDOW_WIDTH
from spacerace.scenes.scene_manager import INITIAL_SCENE, get_next_scene
from spacerace.utils.graphic import begin_center_screen, end_center_screen


def main():
    pr.set_config_flags(pr.ConfigFlags.FLAG_MSAA_4X_HINT)
    pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME)
    pr.set_target_fps(FRAME_RATE)
    pr.hide_cursor()
    pr.init_audio_device()

    scene = INITIAL_SCENE
    scene.init()

    while not pr.window_should_close():
        scene = get_next_scene(scene)

        scene.update(pr.get_frame_time())

        pr.begin_drawing()
        begin_center_screen()
        scene.draw()
        end_center_screen()
        pr.end_drawing()

    scene.release()

    pr.close_window()


if __name__ == "__main__":
    main()

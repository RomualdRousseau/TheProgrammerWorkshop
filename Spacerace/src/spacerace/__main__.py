import pyray as pr

from spacerace import APP_NAME, WINDOW_HEIGHT, WINDOW_WIDTH
from spacerace.scenes.scene_manager import INITIAL_SCENE, get_next_scene


def main():
    pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME)

    scene = INITIAL_SCENE
    scene.init()

    while not pr.window_should_close():
        scene = get_next_scene(scene)

        scene.update(pr.get_frame_time())

        pr.begin_drawing()
        scene.draw()
        pr.end_drawing()

    scene.release()

    pr.close_window()


if __name__ == "__main__":
    main()

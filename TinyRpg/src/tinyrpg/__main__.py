import pyray as pr

from tinyrpg.constants import APP_NAME, FRAME_RATE, WINDOW_HEIGHT, WINDOW_WIDTH
from tinyrpg.engine import FadeInOut, Scene, change_scene
from tinyrpg.scenes import Game, intro, menu


def main():
    pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME)
    pr.set_target_fps(FRAME_RATE)
    pr.init_audio_device()
    pr.set_exit_key(pr.KeyboardKey.KEY_END)

    transition_table: dict[str, dict[str, Scene]] = {
        "intro": {"keypress": FadeInOut("menu", menu)},
        "menu": {"keypress": FadeInOut("level1", Game("level1"))},
        "level1": {"goto_level": FadeInOut("level1", Game("level2"))},
        "level2": {"goto_level": FadeInOut("level2", Game("level1"))},
    }

    scene: Scene = intro
    scene.init()

    while not pr.window_should_close():
        scene.update(pr.get_frame_time())

        pr.begin_drawing()
        scene.draw()
        pr.end_drawing()

        scene = change_scene(scene, transition_table)

    scene.release()

    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()

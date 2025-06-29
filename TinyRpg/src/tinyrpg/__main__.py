import pyray as pr

from tinyrpg.constants import APP_NAME, FRAME_RATE, WINDOW_HEIGHT, WINDOW_WIDTH
from tinyrpg.engine import Scene, change_scene
from tinyrpg.scenes import FadeInOut, get_game, intro


def main():
    pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME)
    pr.set_target_fps(FRAME_RATE)
    pr.init_audio_device()
    pr.set_exit_key(pr.KeyboardKey.KEY_END)

    scene: Scene = intro
    scene.init()

    t: dict[str, dict[str, Scene]] = {
        "intro": {"keypress": FadeInOut("transition1", intro, get_game("level1"))},
        "transition1": {"complete": get_game("level1")},
        "level1": {"gameover": FadeInOut("transition2", get_game("level1"), get_game("level2"))},
        "transition2": {"complete": get_game("level2")},
        "level2": {"gameover": FadeInOut("transition3", get_game("level2"), intro)},
        "transition3": {"complete": intro},
    }

    while not pr.window_should_close():
        scene.update(pr.get_frame_time())

        pr.begin_drawing()
        scene.draw()
        pr.end_drawing()

        scene = change_scene(scene, t)

    scene.release()

    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()

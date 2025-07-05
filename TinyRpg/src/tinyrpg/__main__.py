import pyray as pr

from tinyrpg.constants import APP_NAME, FRAME_RATE, WINDOW_HEIGHT, WINDOW_WIDTH
from tinyrpg.engine import FadeInOut, Scene, SceneEvent, change_scene, pop_scene
from tinyrpg.scenes import Game, Menu, intro, load_states, reset_states, save_states

INITIAL_STATE: Scene = intro

STATES: dict[str, Scene] = {
    "intro": intro,
    "menu": FadeInOut("menu", Menu()),
    "level1": FadeInOut("level1", Game("level1")),
    "level2": FadeInOut("level2", Game("level2")),
}

TRANSITION_TABLE: dict[str, dict[str, Scene]] = {
    "intro": {"keypress": STATES["menu"]},
    "menu": {"keypress": STATES["level1"]},
    "level1": {"goto_level": STATES["level2"], "goto_menu": STATES["menu"]},
    "level2": {"goto_level": STATES["level1"], "goto_menu": STATES["menu"]},
}


def main():
    pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME)
    pr.set_target_fps(FRAME_RATE)
    pr.init_audio_device()
    pr.set_exit_key(pr.KeyboardKey.KEY_END)

    scene: Scene = INITIAL_STATE
    scene.init()

    request_close = False

    while not pr.window_should_close() and not request_close:
        scene.update(pr.get_frame_time())

        pr.begin_drawing()
        scene.draw()
        pr.end_drawing()

        while (event := scene.next_event()) is not None:
            match event:
                case SceneEvent("change", (state, input)):
                    scene = change_scene(scene, state, input, TRANSITION_TABLE)
                case SceneEvent("pop", ()):
                    scene = pop_scene(scene)
                case SceneEvent("reset", ()):
                    reset_states(STATES)
                case SceneEvent("save", ()):
                    save_states("saved/state.pkl", STATES)
                case SceneEvent("load", ()):
                    load_states("saved/state.pkl", STATES)
                case SceneEvent("quit", ()):
                    request_close = True

    scene.release()

    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()

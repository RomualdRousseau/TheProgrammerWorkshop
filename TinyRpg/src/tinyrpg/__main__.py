import pyray as pr

from tinyrpg.constants import APP_NAME, FRAME_RATE, WINDOW_HEIGHT, WINDOW_WIDTH
from tinyrpg.engine import FadeInOut, Scene, process_scene_event
from tinyrpg.scenes import Game, GameOver, Menu, intro

INITIAL_STATE: Scene = intro

STATES: dict[str, Scene] = {
    "intro": intro,
    "menu": FadeInOut("menu", Menu()),
    "level1": FadeInOut("level1", Game("level1")),
    "level2": FadeInOut("level2", Game("level2")),
    "menu_level": FadeInOut("menu_level", Menu(with_save = True)),
    "game_over_win": FadeInOut("game_over_win", GameOver("WIN", pr.WHITE)),
    "game_over_lost": FadeInOut("game_over_lost", GameOver("LOST", pr.BLACK)),
}

TRANSITION_TABLE: dict[str, dict[str, Scene]] = {
    "intro": {"keypress": STATES["menu"]},
    "menu": {"goto_level1": STATES["level1"]},
    "level1": {
        "goto_level2": STATES["level2"],
        "goto_menu": STATES["menu_level"],
        "goto_game_over_win": STATES["game_over_win"],
        "goto_game_over_lost": STATES["game_over_lost"],
    },
    "level2": {
        "goto_level1": STATES["level1"],
        "goto_menu": STATES["menu_level"],
        "goto_game_over_win": STATES["game_over_win"],
        "goto_game_over_lost": STATES["game_over_lost"],
    },
    "menu_level": {},
    "game_over_win": {},
    "game_over_lost": {},
}


def main():
    pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME)
    pr.set_target_fps(FRAME_RATE)
    pr.init_audio_device()
    pr.set_exit_key(pr.KeyboardKey.KEY_END)

    scene: Scene = INITIAL_STATE
    scene.init()

    should_close = False

    while not pr.window_should_close() and not should_close:
        scene.update(pr.get_frame_time())

        pr.begin_drawing()
        scene.draw()
        pr.end_drawing()

        while (event := scene.next_event()) is not None:
            scene, should_close = process_scene_event(event, scene, STATES, TRANSITION_TABLE)

    scene.release()

    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()

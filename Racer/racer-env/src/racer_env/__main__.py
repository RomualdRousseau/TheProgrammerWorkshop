import fire
import pyray as pr

from racer_env.core.config import Config
from racer_env.core.input import KeyboardInput, RandomInput
from racer_env.core.scene_manager import SceneManager
from racer_env.game.gameplay import init_gameplay_state
from racer_env.game.scenes import SimulationScene, StartScene


def play():
    """Run the environment with human controls (Raylib)."""
    scene_manager, state = SceneManager(), None
    scene_manager.transition_to(StartScene())

    pr.init_window(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, "Racer RL")
    pr.set_target_fps(Config.TARGET_FPS)

    while not pr.window_should_close():
        dt = pr.get_frame_time()
        state = scene_manager.update(dt, state, KeyboardInput())

        pr.begin_drawing()
        scene_manager.draw(state)
        pr.end_drawing()

    pr.close_window()


def test():
    """Run the environment with a random agent (Simulation mode)."""
    scene_manager, state = SceneManager(), init_gameplay_state()
    scene_manager.transition_to(SimulationScene())

    pr.init_window(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, "Racer RL - Test")
    pr.set_target_fps(Config.TARGET_FPS)

    while not (pr.window_should_close() or state.game_over or state.won):
        dt = pr.get_frame_time()
        state = scene_manager.update(dt, state, RandomInput())

        pr.begin_drawing()
        scene_manager.draw(state)
        pr.end_drawing()

    pr.close_window()


def main():
    fire.Fire(
        {
            "play": play,
            "test": test,
        }
    )


if __name__ == "__main__":
    main()

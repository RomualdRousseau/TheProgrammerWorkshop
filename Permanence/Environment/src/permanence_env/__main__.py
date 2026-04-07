"""
Main entry point for the permanence_env simulation.

This module initializes the game state and handles the main simulation loop.
"""

import random
import pyray as pr
from permanence_env.game.gameplay import update_game, init_game
from permanence_env.ui.renderer import draw_game
from permanence_env.utils.constant import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WINDOW_TITLE,
)
from permanence_env.core.config import config


def main() -> None:
    """
    Primary application loop: initializes window, state, and runs update/draw cycle.
    """
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    pr.set_target_fps(config.target_fps)

    state = init_game()
    initial_speed = random.uniform(20.0, 100.0)

    while not pr.window_should_close():
        dt = pr.get_frame_time()

        # Update simulation logic
        state = update_game(state, dt, initial_speed)

        # Rendering
        draw_game(state)

    pr.close_window()


if __name__ == "__main__":
    main()

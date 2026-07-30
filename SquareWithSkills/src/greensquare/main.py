"""Composition root wiring engine adapters into gameplay loop."""

from greensquare.engine.raylib_engine import RaylibEngine
from greensquare.game.gameplay import init_player, update_game


def run() -> None:
    """Initialize engine and run the main game loop."""
    engine = RaylibEngine()
    engine.init_window()

    player = init_player()

    while not engine.window_should_close():
        input_state = engine.poll_input()
        if input_state.should_quit:
            break

        dt = engine.get_frame_time()
        player = update_game(player, input_state, dt)

        engine.begin_frame()
        engine.render_game(player)
        engine.end_frame()

    engine.close_window()


if __name__ == "__main__":
    run()

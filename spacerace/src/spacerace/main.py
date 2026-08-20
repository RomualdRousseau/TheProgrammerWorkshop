"""Composition root: wires the Raylib engine into the scene router and runs the loop."""

from spacerace.core.input import InputCommand
from spacerace.core.state import AppState, Scene
from spacerace.engine import raylib_input, raylib_render
from spacerace.game import scenes

_MAX_FRAME_TIME: float = 0.1  # clamp dt spikes (e.g. window dragging)


def run() -> None:
    """Open the window and run the frame loop until the user quits."""
    raylib_render.init()
    state = scenes.init()
    while not raylib_render.should_quit():
        dt = min(raylib_render.get_frame_time(), _MAX_FRAME_TIME)
        command = _poll_command(state, dt)
        state = scenes.update(command, state, dt)
        scenes.draw(raylib_render, state)
    raylib_render.close()


def _poll_command(state: AppState, dt: float) -> InputCommand:
    """Use keyboard input unless the demo bot is driving."""
    keyboard = raylib_input.poll(dt)
    if state.scene == Scene.DEMO:
        assert state.demo is not None
        if keyboard.confirm or _any_mapped_key(keyboard):
            return keyboard
        return state.demo.bot.poll(dt)
    return keyboard


def _any_mapped_key(command: InputCommand) -> bool:
    return command.p1_up or command.p1_down or command.p2_up or command.p2_down


if __name__ == "__main__":
    run()

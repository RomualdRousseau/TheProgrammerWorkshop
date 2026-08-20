"""Composition root: wires the Raylib engine into the game and runs the loop."""

from spacerace.engine import raylib_input, raylib_render
from spacerace.game import gameplay

_MAX_FRAME_TIME: float = 0.1  # clamp dt spikes (e.g. window dragging)


def run() -> None:
    """Open the window and run the frame loop until the user quits."""
    raylib_render.init()
    state = gameplay.init()
    while not raylib_render.should_quit():
        dt = min(raylib_render.get_frame_time(), _MAX_FRAME_TIME)
        command = raylib_input.poll(dt)
        state = gameplay.update(command, state, dt)
        raylib_render.begin_frame()
        gameplay.draw(raylib_render, state)
        raylib_render.end_frame()
    raylib_render.close()


if __name__ == "__main__":
    run()

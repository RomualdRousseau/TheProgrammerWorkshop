"""Headless gameplay loop tests using mock engine injection."""

from greensquare.core.state import InputState, PlayerState
from greensquare.game.gameplay import init_player, update_game


class MockInput:
    def __init__(self, inputs: list[InputState]) -> None:
        self.inputs = inputs
        self.index = 0

    def poll_input(self) -> InputState:
        if self.index < len(self.inputs):
            state = self.inputs[self.index]
            self.index += 1
            return state
        return InputState()


class MockRender:
    def __init__(self) -> None:
        self.rendered_states: list[PlayerState] = []

    def render_game(self, player: PlayerState) -> None:
        self.rendered_states.append(player)


def test_headless_gameplay_loop() -> None:
    inputs = [
        InputState(move_x=1.0, move_y=0.0),  # Frame 1: move right
        InputState(move_x=0.0, move_y=1.0),  # Frame 2: move down
        InputState(should_quit=True),  # Frame 3: quit
    ]

    mock_input = MockInput(inputs)
    mock_render = MockRender()

    player = init_player()
    dt = 0.1

    while True:
        input_state = mock_input.poll_input()
        if input_state.should_quit:
            break

        player = update_game(player, input_state, dt)
        mock_render.render_game(player)

    assert len(mock_render.rendered_states) == 2
    # Frame 1: x increases from initial 240
    assert mock_render.rendered_states[0].x > 240.0
    # Frame 2: y increases from initial 240
    assert mock_render.rendered_states[1].y > 240.0

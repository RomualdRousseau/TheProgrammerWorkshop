"""Raylib hardware adapter implementing InputEngine and RenderEngine protocols."""

import pyray as pr
from greensquare.core.constant import PLAYER_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
from greensquare.core.state import InputState, PlayerState
from greensquare.engine.config import TARGET_FPS, WINDOW_TITLE


class RaylibEngine:
    """Concrete Raylib adapter for input and rendering."""

    def init_window(self) -> None:
        pr.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        pr.set_target_fps(TARGET_FPS)

    def close_window(self) -> None:
        pr.close_window()

    def window_should_close(self) -> bool:
        return bool(pr.window_should_close())

    def get_frame_time(self) -> float:
        return float(pr.get_frame_time())

    def poll_input(self) -> InputState:
        move_x = 0.0
        move_y = 0.0

        if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):  # type: ignore[attr-defined]
            move_x += 1.0
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):  # type: ignore[attr-defined]
            move_x -= 1.0

        if pr.is_key_down(pr.KeyboardKey.KEY_DOWN):  # type: ignore[attr-defined]
            move_y += 1.0
        if pr.is_key_down(pr.KeyboardKey.KEY_UP):  # type: ignore[attr-defined]
            move_y -= 1.0

        should_quit = bool(
            pr.is_key_pressed(pr.KeyboardKey.KEY_ESCAPE)  # type: ignore[attr-defined]
            or pr.window_should_close()
        )

        return InputState(
            move_x=move_x,
            move_y=move_y,
            should_quit=should_quit,
        )

    def begin_frame(self) -> None:
        pr.begin_drawing()

    def render_game(self, player: PlayerState) -> None:
        pr.clear_background(pr.BLACK)

        # Render fading motion trail
        trail_count = len(player.trail)
        for i, (tx, ty) in enumerate(player.trail):
            alpha = int(120 * (1.0 - (i + 1) / (trail_count + 1)))
            trail_color = pr.Color(0, 200, 50, alpha)
            pr.draw_rectangle(
                int(tx),
                int(ty),
                PLAYER_SIZE,
                PLAYER_SIZE,
                trail_color,
            )

        # Render soft drop shadow behind player
        shadow_offset = 6
        shadow_color = pr.Color(10, 30, 10, 160)
        pr.draw_rectangle(
            int(player.x + shadow_offset),
            int(player.y + shadow_offset),
            PLAYER_SIZE,
            PLAYER_SIZE,
            shadow_color,
        )

        # Render main player square
        pr.draw_rectangle(
            int(player.x),
            int(player.y),
            PLAYER_SIZE,
            PLAYER_SIZE,
            pr.GREEN,
        )

    def end_frame(self) -> None:
        pr.end_drawing()

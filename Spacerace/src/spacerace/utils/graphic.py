import pyray as pr

from spacerace import WINDOW_HEIGHT, WINDOW_WIDTH


def begin_center_screen():
    offx = max(pr.get_screen_width() - WINDOW_WIDTH, 0) // 2
    offy = max(pr.get_screen_height() - WINDOW_HEIGHT, 0) // 2
    pr.rl_set_matrix_modelview(pr.matrix_translate(offx, offy, 0))
    pr.begin_scissor_mode(offx, offy, WINDOW_WIDTH, WINDOW_HEIGHT)


def end_center_screen():
    pr.end_scissor_mode()
    pr.rl_set_matrix_modelview(pr.matrix_translate(0, 0, 0))


def draw_text_centered(message: str, x: int, y: int, font_size: int, color: pr.Color = pr.RAYWHITE):
    msg_size = pr.measure_text(message, font_size)
    pr.draw_text(message, x - msg_size // 2, y - font_size // 2, font_size, color)

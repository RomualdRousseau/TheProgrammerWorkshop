import pyray as pr


def draw_text_centered(message: str, x: int, y: int, font_size: int, color: pr.Color = pr.RAYWHITE):
    msg_size = pr.measure_text(message, font_size)
    pr.draw_text(message, x - msg_size // 2, y - font_size // 2, font_size, color)

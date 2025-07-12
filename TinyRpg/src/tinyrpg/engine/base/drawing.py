import pyray as pr

from tinyrpg.constants import DIR8


def draw_text_outlined_v(text: str, pos: pr.Vector2, font_size: int, fg_color: pr.Color, bg_color: pr.Color):
    for dir in DIR8:
        pr.draw_text(text, int(pos.x + dir[0]), int(pos.y + dir[1]), font_size, bg_color)
    pr.draw_text(text, int(pos.x), int(pos.y), font_size, fg_color)

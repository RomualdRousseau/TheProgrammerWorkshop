import pyray as pr

from tinyrpg.engine.base.widget import Widget

COMPONENT_MARGIN = 1  # px
COMPONENT_PADDING = 1  # px
COMPONENT_BORDER = 1  # px


class Component(Widget):
    def __init__(self):
        super().__init__(pr.vector2_zero(), pr.vector2_one())

    def get_rect(self) -> pr.Rectangle:
        rect = super().get_rect()
        rect.x += COMPONENT_MARGIN
        rect.y += COMPONENT_MARGIN
        rect.width -= 2 * COMPONENT_MARGIN
        rect.height -= 2 * COMPONENT_MARGIN
        return rect

    def get_inner_rect(self) -> pr.Rectangle:
        inner_rect = self.get_rect()
        inner_rect.x += COMPONENT_BORDER + COMPONENT_PADDING
        inner_rect.y += COMPONENT_BORDER + COMPONENT_PADDING
        inner_rect.width -= 2 * (COMPONENT_BORDER + COMPONENT_PADDING)
        inner_rect.height -= 2 * (COMPONENT_BORDER + COMPONENT_PADDING)
        return inner_rect

    def draw(self):
        pr.draw_rectangle_lines_ex(self.get_rect(), COMPONENT_BORDER, pr.RAYWHITE)

from __future__ import annotations

import pyray as pr

from tinyrpg.engine.base.widget import Widget


class TableLayout(Widget):
    def __init__(self, rows: int, cols: int):
        super().__init__(pr.vector2_zero(), pr.vector2_one())
        self.rows = rows
        self.cols = cols
        self.widgets: list[Widget] = []

    def get_inner_rect(self) -> pr.Rectangle:
        return self.get_rect()

    def add(self, widget: Widget) -> TableLayout:
        self.widgets.append(widget)
        return self

    def resize(self, pos: pr.Vector2, size: pr.Vector2):
        super().resize(pos, size)

        inner_rect = self.get_inner_rect()

        matrix = [[[0.0, 0.0] for _ in range(self.cols)] for _ in range(self.rows)]

        # Fill fixed widths and heights

        cells = (x for x in self.widgets)
        for i in range(self.rows):
            for j in range(self.cols):
                cell = next(cells, None)
                if cell:
                    if cell.fixed_width > 0:
                        matrix[i][j][0] = cell.fixed_width
                    if cell.fixed_height > 0:
                        matrix[i][j][1] = cell.fixed_height

        # Fill variable widths

        for i in range(self.rows):
            count = self.cols
            width = inner_rect.width
            for j in range(self.cols):
                if matrix[i][j][0] > 0:
                    count -= 1
                    width -= matrix[i][j][0]
            if count > 0:
                width /= count
                for j in range(self.cols):
                    if matrix[i][j][0] == 0:
                        matrix[i][j][0] = width

        # Fill variable heights

        count = self.rows
        height = inner_rect.height
        for i in range(self.rows):
            h_max = 0
            for j in range(self.cols):
                if h_max < matrix[i][j][1]:
                    h_max = matrix[i][j][1]
            if h_max > 0:
                for j in range(self.cols):
                    if matrix[i][j][1] == 0:
                        matrix[i][j][1] = h_max
                count -= 1
                height -= h_max
        if count > 0:
            height /= count
            for i in range(self.rows):
                for j in range(self.cols):
                    if matrix[i][j][1] == 0:
                        matrix[i][j][1] = height

        cells = (x for x in self.widgets)
        pos = pr.Vector2(inner_rect.x, inner_rect.y)
        for i in range(self.rows):
            h_max = 0
            for j in range(self.cols):
                size = pr.Vector2(*matrix[i][j])
                if h_max < size.y:
                    h_max = size.y

                cell = next(cells, None)
                if cell:
                    cell.resize(pos, size)

                pos = pr.vector2_add(pos, (size.x, 0))
            pos = pr.Vector2(inner_rect.x, pos.y + h_max)

    def draw(self):
        for widget in self.widgets:
            widget.draw()

from tinyrpg.engine import Widget


class DialogEffect(Widget):
    def __init__(self, widgets: list[Widget]):
        super().__init__(widgets[0].pos, widgets[0].size)
        self.widgets = widgets
        self.current = 0

    def update(self, dt: float):
        self.widgets[self.current].update(dt)
        if self.widgets[self.current].closed:
            self.current += 1
            if self.current >= len(self.widgets):
                self.current = len(self.widgets) - 1
                self.close()

    def draw(self):
        self.widgets[self.current].draw()

from tinyrpg.engine.widget import Widget
from tinyrpg.widgets.message import MessageBox


class DialogBox(Widget):
    def __init__(self, messages: list[MessageBox]):
        super().__init__(messages[0].pos, messages[0].size)
        self.messages = messages
        self.current = 0

    def update(self, dt: float):
        self.messages[self.current].update(dt)
        if self.messages[self.current].closed:
            self.current += 1
            if self.current >= len(self.messages):
                self.current = len(self.messages) - 1
                self.closed = True

    def draw(self):
        self.messages[self.current].draw()

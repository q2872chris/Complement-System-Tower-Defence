import pyglet as py

class button1(py.gui.PushButton):
    def __init__(self, *args, text="test", **kwargs):
        super().__init__(*args, **kwargs)
        self.label = py.text.Label(text,
                                   font_name='Times New Roman',
                                   font_size=10,
                                   x=self.x + self.width / 2,
                                   y=self.y + self.width / 2,
                                   batch=self._batch,
                                   anchor_y="center",
                                   anchor_x="center")

    def on_press(self):
        print("button_press")

    def on_release(self):
        pass








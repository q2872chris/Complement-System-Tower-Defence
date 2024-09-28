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



class Scroller:
    def __init__(self, sprite, min_y, max_y):
        self.x = sprite.x
        self.y = sprite.y
        self.sprite = sprite
        self.min_y = min_y
        self.max_y = max_y
        self.width = sprite.width
        self.height = sprite.height
        self.drag = False

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.x < x < self.x + self.width and \
                self.min_y < y < self.max_y:
            print("scroll")

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.drag:
            print("drag")

    def on_mouse_press(self, x, y, button, modifiers):
        if (x, y) in self.sprite:
            self.drag = True

    def on_mouse_release(self, x, y, button, modifiers):
        self.drag = False






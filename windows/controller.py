import pyglet as py
from windows.window_base import WindowBase
from utilities import extend
from globals import game_attrs


class Controller(WindowBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mouse = game_attrs.mouse
        self.scroll_time = 0

    @extend
    def update(self, dt: float):
        self.check_scrolling()

    def on_draw(self):
        self.clear()
        py.gl.glClearColor(0, 0.7, 1, 1)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.update(x=x, y=y)

    def on_mouse_press(self, x, y, b, m):
        self.mouse.update(x=x, y=y, click=True)

    def on_mouse_release(self, x, y, b, m):
        self.mouse.update(click=False)

    def on_mouse_drag(self, x, y, dx, dy, b, m):
        self.mouse.update(x=x, y=y, click=True, dx=dx, dy=dy)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.scroll_time = py.clock.get_default().time()
        self.mouse.update(scroll=True, dx=scroll_x, dy=scroll_y)

    def check_scrolling(self):
        if 0.05 < py.clock.get_default().time() - self.scroll_time:
            self.mouse.update(scroll=False)



if __name__ == "__main__":
    Controller(width=900, height=600, resizable=False, fullscreen=False,
               caption="controller test")
    py.app.run()

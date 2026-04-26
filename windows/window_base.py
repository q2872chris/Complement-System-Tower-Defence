import pyglet as py


class WindowBase(py.window.Window):
    def __init__(self, *args, x=0.0, y=0.9, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_rate = 60
        self.set_cursor("CURSOR_CROSSHAIR")
        self.screen_recentre(x, y)
        py.clock.schedule_interval(self.update, 1 / self.frame_rate)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case py.window.key.ESCAPE:
                self.close()

    def update(self, dt: float):
        pass

    def screen_recentre(self, x: float, y: float):
        """x,y in [-1,1]"""
        x_middle = (self.screen.width - self.width) / 2
        y_middle = (self.screen.height - self.height) / 2 - 10
        x_scaled = int(x_middle * (x + 1))
        y_scaled = int(y_middle * (1 - y * 350 / self.height))
        self.set_location(x_scaled, y_scaled)

    def set_cursor(self, cursor_str="CURSOR_DEFAULT"):
        cursor_id = getattr(self, cursor_str, self.CURSOR_DEFAULT)
        cursor = self.get_system_mouse_cursor(cursor_id)
        self.set_mouse_cursor(cursor)



if __name__ == "__main__":
    WindowBase(width=600, height=400, caption="window test")
    py.app.run()







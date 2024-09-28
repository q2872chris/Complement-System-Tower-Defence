import pyglet as py
from files import game, panel, components, utilities, proteins, initialise
from files.data import window_data as win
from pyglet.window import key

class window(py.window.Window):
    def __init__(self, *args, **kwargs):
        # schedule_interval_for_duration
        super().__init__(*args, **kwargs)
        self.set_caption("Cats ftw")
        self.set_location(340, 40)
        self.set_mouse_cursor(self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR))
        self.keys = key.KeyStateHandler()
        self.track = components.track()
        self.panel_text = utilities.panel_text()
        self.game = game.game(towers := [])
        self.unlock_text = utilities.flash(font_size=70, x=win.game_width / 2,
                                           bold=True, y=win.window_height / 2)
        # self.unlock_text.update(visible=False)
        proteins.protein.update_kwargs(towers=towers, track=self.track.outer_sprites,
            unlock_text=self.unlock_text)
        grid, speed = initialise.shop_grid()
        self.panel = panel.panel(grid, speed, self.panel_text)
        self.main_game_running = True

        # more work needs to be done to allow C1 to cleave both C4 into C4b and C4a, and to
        # cleave C4bC2 into C4bC2b and C2a!

        # pause and clean up everything!!!!!!!!!!! seriously
        # better linking between modules!
        # other text, create proper system

        # sprites and animations:
        #   - image grids, texture grids
        #   - sprite sheet

        # clever group assignment

    def on_draw(self):
        self.clear()
        py.gl.glClearColor(0, 0.7, 1, 1)
        self.push_handlers(self.keys)
        if self.main_game_running:
            self.unlock_text.animate()
            win.batch.draw()
        # print(py.clock.get_fps())

    def on_mouse_motion(self, x, y, dx, dy):
        if self.main_game_running:
            self.panel.update(x, y, 0, False)
            self.game.update(x, y, False)

    def on_mouse_press(self, x, y, b, m):
        if self.main_game_running:
            self.panel.update(x, y, 0, True)
            self.game.update(x, y, True)

    def on_mouse_release(self, x, y, b, m):
        if self.main_game_running:
            self.panel.update(x, y, 0, False)
            self.game.update(x, y, False)

    def on_mouse_drag(self, x, y, dx, dy, b, m):
        if self.main_game_running:
            self.panel.update(x, y, dy, True)

    def on_mouse_scroll(self, x, y, dx, dy):
        if self.main_game_running:
            self.panel.update(x, y, dy, False)
            self.panel.scroll(x, y, dy)

    def on_key_press(self, k, m):
        match k:
            case key.ESCAPE:
                self.close()
            case _:
                pass

    def on_key_release(self, k, m):
        pass

    def on_text(self, t):
        pass

    def on_resize(self, width, height):
        win.update(width, height)

from pyglet import shapes
from files.utilities import text, button
from files.data import window_data as win, game_data

border_colour = (0, 0, 40)
top_panel_fill = (100, 0, 0)
side_panel_fill = (50, 0, 0)


class tower_panel:
    def __init__(self):
        self.name = text(7, bold=True, font_size=30, color=(255, 255, 0, 250),
                         y=win.window_height - win.top_panel_height / 2)
        self.info = button(7, "info", italic=True, font_size=20, color=(100, 0, 200, 255),
                           y=win.top_panel_height * 0.3, hover_font_size=22, hover_color=(100, 0, 240, 255))
        self.cleave = button(7, "cleave", italic=True, font_size=20, color=(100, 40, 200, 255),
                             y=win.top_panel_height * 0.5, hover_font_size=22, hover_color=(100, 50, 240, 255))
        self.top = shapes.BorderedRectangle(win.game_width, win.grid_panel_height, win.grid_panel_width,
            win.top_panel_height, win.panel_border_width, top_panel_fill, border_colour, win.batch, win.groups[6])
        self.side = shapes.BorderedRectangle(win.game_width, 0, win.grid_panel_width, win.grid_panel_height,
            win.panel_border_width, side_panel_fill, border_colour, win.batch, win.groups[6])
        self.info_text = text(7, font_size=15, multiline=True, width=win.grid_panel_width * 0.9,
                              anchor_x="left", anchor_y="top", y=win.grid_panel_height * 0.99)
        self.on = False
        self.info_on = False
        self.cleave_pressed = False
        self.tower = None
        self.reset()

    def reset(self):
        self.on = False
        self.top.visible = False
        self.side.visible = False
        self.info_on = False
        self.name.update_text("")
        self.info_text.update(visible=False)
        self.info.update(visible=False)
        self.cleave.update(visible=False)
        game_data.tower_panel_allow_scroll = True
        if self.tower is not None:
            self.tower.update_view()
            self.tower = None

    def set(self, x, tower):
        if self.tower is not None:
            self.tower.update_view()
        self.tower = tower
        self.tower.update_view()
        self.name.update_text(tower.name)
        self.info_text.update(text=tower.info)
        if self.tower.cleave[0]:                        # hide cleave if info on?
            self.cleave.update(visible=True)
        else:
            self.cleave.update(visible=False)
        if not self.on:
            self.on = True
            self.top.visible = True
            self.side.visible = True
            self.info.update(visible=True)
            if x < win.game_width / 2:    # make function for changing many x_coordinates
                self.top.x = win.game_width
                self.side.x = win.game_width
                game_data.tower_panel_allow_scroll = False
                self.name.update(x=win.game_width + win.grid_panel_width / 2)
                self.info.update(x=win.game_width + win.grid_panel_width / 2)
                self.cleave.update(x=win.game_width + win.grid_panel_width / 2)
                self.info_text.update(x=win.game_width + win.grid_panel_width * 0.05)
            else:
                self.top.x = 0
                self.side.x = 0
                self.name.update(x=win.grid_panel_width / 2)
                self.info.update(x=win.grid_panel_width / 2)
                self.cleave.update(x=win.grid_panel_width / 2)
                self.info_text.update(x=win.grid_panel_width * 0.05)

    def __contains__(self, item):
        return item in self.side or item in self.top

    def update(self, x, y, click):
        if self.tower.cleave[0] and self.cleave.hover(x, y) and click:
            self.tower.activate_cleave()
            return True
        if self.info.hover(x, y) and click:
            self.info_text.update(visible=not self.info_text.label.visible)
        return False




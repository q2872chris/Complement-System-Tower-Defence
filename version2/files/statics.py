from pyglet.shapes import *
from files.data import window_data as win

"""
"""
border_colour = (0, 0, 40)
top_panel_fill = (100, 0, 0)
side_bar_fill = (50, 0, 0)


class static_sprite:
    def __init__(self):
        self.sprite = None

    def __getattr__(self, item):
        return getattr(self.sprite, item)

    def __contains__(self, item):
        return item in self.sprite


class border(static_sprite):
    def __init__(self):
        super().__init__()
        x, y = win.window_size
        p = [(0, 0), (x, 0), (x, y), (0, y), (0, 0)]
        self.sprite = [Line(*p[i - 1], *p[i], win.border_width, border_colour,
                       win.batch, win.groups[-1]) for i in range(1, len(p))]


class top_panel(static_sprite):
    def __init__(self):
        super().__init__()
        self.sprite = BorderedRectangle(win.game_width, win.grid_panel_height, win.grid_panel_width,
                                        win.top_panel_height, win.panel_border_width, top_panel_fill,
                                        border_colour, win.batch, win.groups[5])


class side_bar(static_sprite):
    def __init__(self):
        super().__init__()
        self.sprite = BorderedRectangle(win.window_width - win.side_bar_width, 0, win.side_bar_width,
                                        win.window_height, win.panel_border_width, side_bar_fill,
                                        border_colour, win.batch, win.groups[0])


class side_panel(static_sprite):
    def __init__(self):
        super().__init__()
        self.sprite = BorderedRectangle(win.game_width, 0, win.grid_panel_width,
            win.grid_panel_height, win.panel_border_width, top_panel_fill,
            border_colour, win.batch, win.groups[0])


def generate_statics():
    return [side_panel(), side_bar(), top_panel(), border()]



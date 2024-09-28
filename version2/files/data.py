import pyglet as py

class window_data:
    x = 900     # default screen width to base resizing on
    y = 600     # default screen height to base resizing on
    groups = [py.graphics.Group(order=i) for i in range(9)]
    batch = py.graphics.Batch()
    border_width = 5
    panel_border_width = 5
    grid_panel_width = 200
    top_panel_height = 150
    side_bar_width = 20
    box_opacity = 200
    game_width: int
    window_height: int
    window_width: int
    window_size: tuple[int, int]
    grid_panel_height: int
    box_width: int
    scroller_radius: float

    @classmethod
    def initialise(cls, x: int, y: int):
        cls.game_width = x - cls.grid_panel_width
        cls.window_size = (x, y)
        cls.window_width = x
        cls.window_height = y
        cls.grid_panel_height = y - cls.top_panel_height
        cls.box_width = (cls.grid_panel_width - cls.side_bar_width) // 2
        cls.scroller_radius = (cls.side_bar_width - cls.border_width / 2) / 2

    @classmethod
    def update(cls, x: int, y: int):  # update upon window resize, need to update whole batch also
        pass


class game_data:
    tower_panel_allow_scroll = False


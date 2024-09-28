from pyglet import shapes
from files.data import window_data as size

# more data for attributes


class tower_range:
    def __init__(self, default_opacity=100):
        self.colour_green = (0, 250, 0)
        self.colour_red = (250, 0, 0)
        self.colour_blue = (0, 0, 250)
        self.sprite = shapes.Circle(0, 0, 0, 30,
            self.colour_red, size.batch, size.groups[5])
        self.default_opacity = default_opacity

    def update(self, x=0, y=0, radius=None, opacity=None, colour=1):
        if opacity is not None:
            self.sprite.opacity = opacity
        if radius is not None:
            self.sprite.radius = radius
        self.sprite.position = (x, y)
        match colour:
            case 0:
                self.sprite.color = self.colour_green
            case 1:
                self.sprite.color = self.colour_red
            case 2:
                self.sprite.color = self.colour_blue


class scroller:     # fix border clash
    def __init__(self, colour=(0, 255, 0, 255)):
        r = size.scroller_radius
        x = size.window_width - size.side_bar_width + r
        y = size.grid_panel_height - r
        self.sprite = shapes.Circle(x, y, r, 20, colour, size.batch, size.groups[3])
        self.max = y
        self.min = r + size.border_width / 2

    def __contains__(self, item: tuple[int, int]):
        return item in self.sprite

    def __getattr__(self, item):
        return getattr(self.sprite, item)

    def update(self, dy):
        y = self.sprite.y + dy
        if y > self.min:
            self.sprite.y = min(y, self.max)
        return y > self.min


class grid_square:      # lock should be invisible, red should be for cost
    def __init__(self, x, y, protein):
        self.locked = False
        self.locked_opacity = 100
        self.max = y
        self.width = size.box_width
        self.sprite = shapes.BorderedRectangle(x, y, self.width, self.width,
            size.panel_border_width, (0, 200, 0, 200), (0, 100, 0, 200), size.batch, size.groups[2])
        self.locked_sprite = shapes.BorderedRectangle(x, y, self.width, self.width,
            size.panel_border_width, (250, 0, 0, 0), (100, 0, 0, 0), size.batch, size.groups[4])
        self.protein = protein

    def __contains__(self, item: tuple[int, int]):
        locked = not self.protein.locked if self.protein is not None else False
        return item in self.sprite and locked

    def update(self, dy):
        y = max(self.sprite.y - dy, self.max)
        self.sprite.y = y
        if self.protein is None:
            return
        self.protein.update_scroll(y + self.width / 2)

    def update_money(self, x):
        if self.protein is None:
            return
        if x < self.protein.cost and not self.protein.locked:
            self.locked_sprite.opacity = self.locked_opacity
            self.locked = True
        else:
            self.locked_sprite.opacity = 0
            self.locked = False


class track:        # try bezier curves
    def __init__(self):
        self.track_points = [(0, 0), (60, 80), (200, 200), (400, 500),
                             (450, 200), (500, 180), (600, 300)]
        self.fill_colour = (55, 255, 55, 255)
        self.border_colour = (100, 100, 100, 255)
        self.inner_width = 20
        self.outer_width = 24
        self.outer_sprites = []
        self.inner_sprites = []
        self.create_track(size.batch, size.groups[0], size.groups[1])

    def create_track(self, batch, group1, group2):
        outer_circle = (self.outer_width / 2, None, self.border_colour, batch, group1)
        inner_circle = (self.inner_width / 2, None, self.fill_colour, batch, group2)
        outer_line = (self.outer_width, self.border_colour, batch, group1)
        inner_line = (self.inner_width, self.fill_colour, batch, group2)
        self.outer_sprites.append(shapes.Circle(*self.track_points[0], *outer_circle))
        self.inner_sprites.append(shapes.Circle(*self.track_points[0], *inner_circle))
        for i in range(1, len(self.track_points)):
            self.outer_sprites.append(shapes.Circle(*self.track_points[i], *outer_circle))
            self.inner_sprites.append(shapes.Circle(*self.track_points[i], *inner_circle))
            self.outer_sprites.append(
                shapes.Line(*self.track_points[i - 1], *self.track_points[i], *outer_line))
            self.inner_sprites.append(
                shapes.Line(*self.track_points[i - 1], *self.track_points[i], *inner_line))

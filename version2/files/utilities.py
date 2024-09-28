from pyglet.text import Label
from files.data import window_data as win
# rename module to something text related

# get rid of this class?
class panel_text:
    def __init__(self):
        name_kwargs = {"x": win.game_width + win.grid_panel_width / 2,
                       "y": win.grid_panel_height + win.top_panel_height * 0.6,
                       "font_size": 30,
                       "color": (255, 255, 0, 255),
                       "bold": True}
        cost_kwargs = {"x": win.game_width + win.grid_panel_width / 2,
                       "y": win.grid_panel_height + win.top_panel_height * 0.4,
                       "font_size": 20,
                       "color": (255, 255, 255, 255),
                       "italic": True}
        combine_kwargs = {"x": win.game_width + win.grid_panel_width / 2,
                          "y": win.grid_panel_height + win.top_panel_height * 0.8,
                          "font_size": 18,
                          "color": (55, 255, 55, 255),
                          "italic": True}
        self.name = text(6, **name_kwargs)
        self.cost = text(6, **cost_kwargs)
        self.combine = text(6, **combine_kwargs)

class text:     #multiline still to be enabled
    def __init__(self, group_id=-1, default_text="", **kwargs):
        default_kwargs = {"anchor_x": "center", "anchor_y": "center",
                          "batch": win.batch, "group": win.groups[group_id]}
        self.label = Label(**dict(default_kwargs, **kwargs))
        self.default_text = default_text
        self.update(text=default_text)

    def update(self, **kwargs):     # more specific functions/class, abstract class?
        for i, j in kwargs.items():
            setattr(self.label, i, j)

    # get size to change based to text length and bounding box width
    def update_text(self, msg=None, default=False):
        if default:
            self.default_text = msg
        self.update(text=msg if msg is not None else self.default_text)


class button(text):
    def __init__(self, group_id=-1, default_text="", **kwargs):
        super_kwargs = {i: kwargs[i] for i in kwargs if i[:6] != "hover_"}
        super().__init__(group_id, default_text, **super_kwargs)
        default_keys = ["font_size", "color"]
        self.hover_kwargs = {k: kwargs["hover_" + k] for k in default_keys}
        self.default_kwargs = {k: kwargs[k] for k in default_keys}

    def hover(self, x, y):
        if (x, y) in self:
            self.update(**self.hover_kwargs)
            return True
        else:
            self.update(**self.default_kwargs)
            return False

    def __contains__(self, pos: tuple[int, int]):
        x, y = pos
        lx, ly = self.label.x, self.label.y
        w, h = self.label.content_width / 2, self.label.content_height * 0.3
        return lx - w < x < lx + w and ly - h * 2 < y < ly


class flash(text):
    def __init__(self, group_id=-1, default_text="", max_time=1, **kwargs):
        super().__init__(group_id, default_text, **kwargs)
        self.inc = 255 / (max_time * 60)
        self.float_opacity = 0
        self.peak = 1
        self.hold_peak = 1      # not implemented
        self.on = False
        self.label.opacity = 0
        self.queue = []

    def start_animation(self, new_text=""):
        if not self.on:
            self.on = True
            self.update(text=new_text)
        else:
            self.queue.append(new_text)

    def animate(self):
        if self.on:
            self.float_opacity += self.inc * self.peak
            self.label.opacity = int(self.float_opacity)
            if self.float_opacity + self.inc > 255:
                self.peak = -1
            elif self.float_opacity - self.inc < 0:
                self.peak = 1
                if len(self.queue) > 0:
                    self.update(text=self.queue.pop(0))
                else:
                    self.on = False


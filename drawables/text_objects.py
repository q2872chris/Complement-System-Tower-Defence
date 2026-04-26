import pyglet as py
from abc import ABC
import numpy as np
from window_objects import Mouse

font = "Times New Roman"


class BaseLabel(py.text.Label, ABC):
    def __init__(self, *args, group=None, **kwargs):
        super().__init__(*args, group=group, **kwargs)
        self.group = group
        self.visible = True

    def set_opacity(self, opacity: int):
        self.color = (*self.color[:3], opacity)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def update_position(self, vec: np.array):
        self.position = self.position + vec  # noqa

    def set_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Label(BaseLabel):
    def __init__(self, text: str, x: int, y: int, size: int, colour: tuple, batch: py.graphics.Batch,
                 group: py.graphics.OrderedGroup, bold=False, italic=False, anchor_x="center",
                 anchor_y="center", width=180, align="left", multiline=False):
        super().__init__(text, font, size, bold, italic, False, colour, x, y,
                         width, None, anchor_x, anchor_y, align, multiline,
                         batch=batch, group=group)


class Button(BaseLabel):
    def __init__(self, text: str, x: int, y: int, size1: int, size2: int,
                 colour1: tuple, colour2: tuple, batch: py.graphics.Batch,
                 group: py.graphics.OrderedGroup, bold=False, italic=False,
                 colour3: tuple = None, colour4: tuple = None,
                 off_action=lambda: None, on_action=lambda: None,
                 quick_action=None, disable_on_click=True, lock_on=False):
        super().__init__(text, font, size1, bold, italic, False, colour1, x, y,
                         200, None, "center", "center", batch=batch, group=group)
        self.size1 = size1
        self.size2 = size2
        colour3 = colour1 if colour3 is None else colour3
        colour4 = colour2 if colour4 is None else colour4
        self.static_colour = colour1
        self.hover_colour = colour2
        self.switch_static_colour = {colour1: colour3, colour3: colour1}
        self.switch_hover_colour = {colour2: colour4, colour4: colour2}
        self.on = False
        self.clicked = False
        self.on_action = on_action
        self.off_action = off_action
        self.focus = lambda: None
        self.disable_on_click = disable_on_click
        self.lock_on = lock_on
        if quick_action is not None:
            self.on_action = self.quick_action(quick_action)

    def quick_action(self, quick_action):
        def inner():
            self.on = False
            if self.disable_on_click:
                self.font_size = self.size1
                self.color = self.static_colour
            self.focus()
            quick_action()
        return inner

    def run_actions(self):
        if self.on:
            self.on_action()
        else:
            self.off_action()

    def switch_colours(self):
        self.on = not self.on
        self.static_colour = self.switch_static_colour[self.static_colour]
        self.hover_colour = self.switch_hover_colour[self.hover_colour]
        self.run_actions()

    def get_half_dimensions(self) -> tuple[float, float]:
        return self.content_width / 2, (self.content_height / 2) * 0.7

    def collide_point(self, x: int, y: int) -> bool:
        w, h = self.get_half_dimensions()
        return self.x - w <= x <= self.x + w and self.y - h <= y <= self.y + h

    def __contains__(self, point: tuple[int, int]) -> bool:
        return self.collide_point(*point)

    def hover(self, mouse: Mouse, focus=""):
        if mouse.pos() in self:
            self.font_size = self.size2
            self.color = self.hover_colour
            if self.on and self.lock_on:
                return
            if mouse.get_click() and not self.clicked:
                mouse.set_focus(focus)
                self.focus = lambda: mouse.release_focus(focus)
                self.clicked = True
                self.switch_colours()
        else:
            self.font_size = self.size1
            self.color = self.static_colour
        if mouse.get_click():
            self.clicked = True
        if not mouse.get_click("", focus) and self.clicked:
            self.clicked = False
            mouse.release_focus(focus)


class ButtonUp(Button):
    def __init__(self, text: str, x: int, y: int, size1: int, size2: int,
                 colour1: tuple, colour2: tuple, batch: py.graphics.Batch,
                 group: py.graphics.OrderedGroup, bold=False, italic=False,
                 colour3: tuple = None, colour4: tuple = None,
                 off_action=lambda: None, on_action=lambda: None,
                 quick_action=None):
        super().__init__(text, x, y, size1, size2, colour1, colour2, batch, group,
                         bold, italic, colour3, colour4, off_action, on_action,
                         quick_action)

    def hover(self, mouse: Mouse, focus=""):
        if mouse.pos() in self:
            self.font_size = self.size2
            self.color = self.hover_colour
            if mouse.click and not self.clicked:
                mouse.set_focus(focus)
                self.clicked = True
        else:
            self.font_size = self.size1
            self.color = self.static_colour
            if mouse.click:
                self.clicked = False
        if not mouse.click and self.clicked:
            self.clicked = False
            mouse.release_focus(focus)
            self.switch_colours()

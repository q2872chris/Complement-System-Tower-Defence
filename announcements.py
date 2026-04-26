import pyglet as py
from drawables import Label

g = py.graphics.OrderedGroup


class Announcement:
    def __init__(self, batch: py.graphics.Batch, announcements_on=True):
        self.message = Label("", 450, 300, 60, (200, 200, 0, 0), batch, g(9),
                             width=700, multiline=True, align="center")
        self.active = False
        self.fade_speed = 5
        self.ascending = 1
        self.queue = []
        self.previous = []
        self.hold = 0  # Non-constant speed
        self.announcements_on = announcements_on

    def activate(self, text: str, once=False):
        if not self.announcements_on:
            return
        if once:
            if text in self.previous:
                return
            self.previous.append(text)
        if self.active:
            self.queue.append(text)
        else:
            self.message.text = text
        self.active = True

    def update(self):
        if self.active:
            opacity = self.message.current_opacity + self.fade_speed * self.ascending
            if opacity > 255:
                self.ascending = -1
                opacity = self.message.current_opacity + self.fade_speed * self.ascending
            self.message.set_opacity(opacity)
            if self.message.current_opacity == 0:
                self.ascending = 1
                if self.queue:
                    self.message.text = self.queue.pop(0)
                else:
                    self.active = False
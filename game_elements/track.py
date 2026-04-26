import pyglet as py
import numpy as np
from drawables import Circle, Line
from globals import game_attrs

g = py.graphics.OrderedGroup


class Track:
    def __init__(self):
        self.points = [
            [60, -20], [60, 150], [100, 100], [300, 100], [60, 500], [450, 500],
            [450, 350], [250, 350], [250, 280], [340, 280], [440, 240], [520, 340],
            [600, 340], [680, 240], [500, 180], [500, -20]
        ]
        self.fill_colour = (55, 255, 55)
        self.border_colour = (100, 100, 100)
        self.inner_width = 30
        self.outer_width = 34
        self.outer_sprites = []
        self.inner_sprites = []
        self.mesh = []
        self.create_track()
        self.create_mesh()
        # self.mesh_circles = [Circle(x, y, 2, (255, 0, 0), game_attrs.batch, g(3))
        #                      for x, y in self.mesh]

    def create_mesh(self, step=10):
        points = np.array(self.points, dtype=float)
        for i in range(len(points) - 1):
            p0, p1 = points[i], points[i + 1]
            n = int(np.linalg.norm(p1 - p0) / step)
            self.mesh.extend(np.linspace(p0, p1, n + 1, endpoint=False))

    def create_track(self):
        batch = game_attrs.batch
        outer_circle = (self.outer_width / 2, self.border_colour, batch, g(1))
        inner_circle = (self.inner_width / 2, self.fill_colour, batch, g(2))
        outer_line = (self.outer_width, self.border_colour, batch, g(1))
        inner_line = (self.inner_width, self.fill_colour, batch, g(2))
        self.outer_sprites.append(Circle(*self.points[0], *outer_circle))
        self.inner_sprites.append(Circle(*self.points[0], *inner_circle))
        for i in range(1, len(self.points)):
            self.outer_sprites += [
                Circle(*self.points[i], *outer_circle),
                Line(*self.points[i - 1], *self.points[i], *outer_line)
            ]
            self.inner_sprites += [
                Circle(*self.points[i], *inner_circle),
                Line(*self.points[i - 1], *self.points[i], *inner_line)
            ]

import pyglet as py
import numpy as np
from abc import ABC, abstractmethod
import pyglet.shapes as shapes
from itertools import product


class BaseShape(ABC):
    def __init__(self, *args, opacity=255, group=None, **kwargs):
        super().__init__(*args, group=group, **kwargs)
        self.group = group
        self.opacity = opacity
        self.visible = True

    def __contains__(self, xy: tuple[int, int]) -> bool:
        return self.collide_point(*xy)

    @abstractmethod
    def collide_point(self, x: int, y: int) -> bool:
        pass

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def update_position(self, vec: np.array):
        self.position = self.position + vec   # noqa


class BRect(BaseShape, shapes.BorderedRectangle):
    def __init__(self, x: int, y: int, width: int, height: int, border=1, colour=(255, 255, 255),
                 border_color=(100, 100, 100), batch: py.graphics.Batch = None,
                 group: py.graphics.OrderedGroup = None, opacity=255):
        super().__init__(x, y, width, height, border, colour, border_color,
                         batch, group=group, opacity=opacity)
        self.border = border

    def collide_point(self, x: int, y: int) -> bool:
        return self.x <= x <= self.x + self.width and \
            self.y <= y <= self.y + self.height


class Rect(BaseShape, shapes.Rectangle):
    def __init__(self, x: int, y: int, width: int, height: int, colour: tuple[int, int, int],
                 batch: py.graphics.Batch = None, group: py.graphics.OrderedGroup = None,
                 opacity=255):
        super().__init__(x, y, width, height, colour, batch, group=group, opacity=opacity)

    def collide_point(self, x: int, y: int) -> bool:
        return self.x <= x <= self.x + self.width and \
            self.y <= y <= self.y + self.height


class Line(BaseShape, shapes.Line):
    def __init__(self, x: int, y: int, x2: int, y2: int, width=1, colour=(255, 255, 255),
                 batch: py.graphics.Batch = None, group: py.graphics.OrderedGroup = None,
                 opacity=255):
        super().__init__(x, y, x2, y2, width, colour, batch, group=group, opacity=opacity)
        self.width = width

    def collide_point(self, x: int, y: int) -> bool:
        start = np.array([x1 := self.x, y1 := self.y])
        end = np.array([x2 := self.x2, y2 := self.y2])
        point = np.array([x, y])
        d = abs(np.cross(end - start, point - start) / np.linalg.norm(end - start))
        w = self.width / 2
        x1, x2 = min(x1, x2) - w, max(x1, x2) + w
        y1, y2 = min(y1, y2) - w, max(y1, y2) + w
        return d <= w - 1 and x1 <= x <= x2 and y1 <= y <= y2


class Circle(BaseShape, shapes.Circle):
    def __init__(self, x: int, y: int, radius: int, colour: tuple[int, int, int],
                 batch: py.graphics.Batch = None, group: py.graphics.OrderedGroup = None,
                 opacity=255):
        super().__init__(x, y, radius, None, colour, batch, group=group, opacity=opacity)

    def collide_point(self, x: int, y: int) -> bool:
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2

    def update(self, x: int, y: int):
        self.position = [x, y]


class Sprite(BaseShape, py.sprite.Sprite):
    """Assumes centered images."""
    def __init__(self, img, x: int, y: int, batch: py.graphics.Batch,
                 group: py.graphics.OrderedGroup, opacity=255, scale=1):
        super().__init__(img, x, y, batch=batch, group=group, opacity=opacity)
        self.scale = scale

    def collide_point(self, x: int, y: int) -> bool:
        w, h = self.get_half_dimensions()
        return self.x - w <= x <= self.x + w and self.y - h <= y <= self.y + h

    def get_points(self, grid=2) -> iter:
        w, h = self.get_half_dimensions()
        x = np.linspace(self.x - w, self.x + w, grid)
        y = np.linspace(self.y - h, self.y + h, grid)
        return product(x, y)

    def get_half_dimensions(self) -> tuple:
        return self.width / 2, self.height / 2

    def inside_rect(self, rect) -> bool:
        w, h = self.get_half_dimensions()
        b = rect.border if hasattr(rect, "border") else 0
        return rect.x + b <= self.x - w and self.x + w <= rect.x + rect.width - b and \
            rect.y + b <= self.y - h and self.y + h <= rect.y + rect.height - b


class Star(BaseShape, shapes.Star):
    def __init__(self, x: int, y: int, outer_radius: int, inner_radius: int,
                 num_spikes: int, colour: tuple[int, int, int], rotation=0,
                 batch: py.graphics.Batch = None,
                 group: py.graphics.OrderedGroup = None, opacity=255):
        super().__init__(x, y, outer_radius, inner_radius, num_spikes, rotation,
                         colour, batch, group=group, opacity=opacity)

    def collide_point(self, x: int, y: int) -> bool:
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.outer_radius ** 2


class Triangle(BaseShape, shapes.Triangle):
    def __init__(self, x: int, y: int, x2: int, y2: int, x3: int, y3: int,
                 colour: tuple[int, int, int], batch: py.graphics.Batch = None,
                 group: py.graphics.OrderedGroup = None, opacity=255):
        super().__init__(x, y, x2, y2, x3, y3, colour, batch, group=group,
                         opacity=opacity)

    def collide_point(self, x: int, y: int) -> bool:
        return False


class RectBorder:
    def __init__(self, x: int, y: int, width: int, height: int, border: int,
                 colour: tuple[int, int, int], batch: py.graphics.Batch,
                 group: py.graphics.OrderedGroup):
        self.border = [
            Line(x, y, x + width, y, border, colour, batch, group),
            Line(x, y, x, y + height, border, colour, batch, group),
            Line(x, y + height, x + width, y + height, border, colour, batch, group),
            Line(x + width, y, x + width, y + height, border, colour, batch, group)
        ]










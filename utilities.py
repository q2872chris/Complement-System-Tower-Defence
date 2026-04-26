import pyglet as py
import numpy as np


def extend(func):
    """Decorator, calls the next superclass's method instead of overriding."""
    def inner(self, *args, **kwargs):
        current_cls = next(filter(
            lambda base: base.__dict__.get(func.__name__) is inner,
            type(self).__mro__
        ))
        getattr(super(current_cls, self), func.__name__)(*args, **kwargs)
        return func(self, *args, **kwargs)
    return inner
# Add error checking for if there is no super method ^


def image_cutter(file_name: str):
    sprite_map = py.image.load(file_name).get_region
    def cut_image(x: int, y: int, width: int, height: int,
                  anchor_x="centre", anchor_y="centre"):
        img = sprite_map(x=x, y=y, width=width, height=height)
        anchors_x = {"centre": width // 2}
        anchors_y = {"centre": height // 2}
        img.anchor_x = anchors_x[anchor_x]
        img.anchor_y = anchors_y[anchor_y]
        return img
    return cut_image


class CustomComplex(complex):
    def __iter__(self):
        return iter((self.real, self.imag))

    def rotate(self, radians: float):
        return CustomComplex(self * np.exp(1j * radians))


def quadratic_solver(a, b, c) -> (tuple[float, float] | None):
    dis = b ** 2 - 4 * a * c
    if dis < 0:
        return None
    sqrt_dis = np.sqrt(dis)
    x1 = (-b + sqrt_dis) / (2 * a)
    x2 = (-b - sqrt_dis) / (2 * a)
    return x1, x2


def safe_sum(iterable: iter) -> iter:
    """Can sum any iterable with items that have compatible __add__ methods,
     for example a list of strings."""
    return sum(iterable[1:], iterable[0])





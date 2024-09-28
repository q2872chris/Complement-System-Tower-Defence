from abc import ABC
from pyglet import shapes
from files.data import window_data as win
# from scipy.spatial import KDTree                 # try this instead of iterating over everything

# game
class tower:
    def __init__(self, x: int, y: int):
        self.attack = 3
        self.circle = shapes.Circle(x, y, self.range, 30,
            (100, 100, 100, 0), win.batch, win.groups[3])

    def update_view(self):
        self.circle.opacity = 0 if self.circle.opacity else 100


# shop, super class/abstract class/mixin class
class protein(ABC):
    shop_proteins = {}
    locked_proteins = {}
    combined_proteins = {}
    group1 = win.groups[7]
    group2 = win.groups[3]
    position = [0, 0]
    towers: list
    unlock_text = None
    current_base = None
    track = None
    width: int
    height: int
    colour: tuple[int, int, int, int]
    sprite = None
    """imported class attributes for subclasses:
            ...
    """
    @classmethod
    def update_kwargs(cls, **kwargs):
        for i, j in kwargs.items():
            setattr(cls, i, j)

    @classmethod
    def spriter(cls, x: int, y: int):
        b = shapes.Rectangle(x, y, cls.width, cls.height, cls.colour, win.batch, cls.group2)
        b.anchor_position = (cls.width / 2, cls.height / 2)
        return b

    @classmethod
    def update_scroll(cls, y: int):
        cls.position[1] = y
        cls.sprite.y = y

    @classmethod
    def place_check(cls, x: int, y: int, inc=5):         # take into account screen border
        cls.current_base = None
        w = cls.width // 2
        points = [*[(x - w, y + i) for i in range(-w, w, inc)],
                  *[(x + w, y + i) for i in range(-w, w, inc)],
                  *[(x + i, y - w) for i in range(-w, w, inc)],
                  *[(x + i, y + w) for i in range(-w, w, inc)],
                  (x, y)]   # perimeter and centre
        tower_intersect = list(filter(lambda i: points in i, cls.towers))
        if len(tower_intersect) > 0:
            bases = list(filter(lambda i: type(i).__name__ in cls.base, tower_intersect))
            if len(bases) > 0:
                distances = {i.distance(cls): i for i in bases}
                cls.current_base = distances[min(distances.keys())]
                return 2
            return 1
        track_check = not any(any(j in i for j in points) for i in cls.track)
        x_bound = w + win.border_width / 2 < x < win.game_width - w
        y_bound = w + win.border_width / 2 < y < win.window_height - w - win.border_width / 2
        return 0 if track_check and x_bound and y_bound else 1

    @classmethod
    def update_pos(cls, x=None, y=None):
        if x is None and y is None:
            cls.sprite.position = cls.position
            cls.sprite.group = cls.group2
        else:
            x1, y1 = cls.sprite.position
            cls.sprite.position = (x or x1, y or y1)
            cls.sprite.group = cls.group1

    @classmethod
    def unlock(cls, cleave=False):
        proteins = cls.cleave if cleave else cls.unlock_tower
        try:
            for i in proteins:
                new = protein.locked_proteins.pop(i)
                protein.shop_proteins[new.__name__] = new
                new.sprite.opacity = 255
                new.locked = False
                text = " cleaved" if cleave else " unlocked"
                cls.unlock_text.start_animation(new.__name__ + text)
        except KeyError:
            pass

    @classmethod
    def return_combination(cls, arg=""):
        combination = cls.combination[cls.base.index(cls.current_base.name)]
        if arg:
            return getattr(cls.combined_proteins[combination], arg)
        return combination

    @classmethod
    def initialise(cls, x: int, y: int):
        if (a := cls.place_check(x, y)) == 2:
            cls.unlock(cleave=True)
            new_class = cls.combined_proteins[cls.return_combination()]
            cls.towers.append(new_class(*cls.current_base.sprite.position))
            cls.current_base.sprite.delete()
            cls.towers.remove(cls.current_base)
        elif a == 0:
            cls.towers.append(cls(x, y))

    def __contains__(self, items) -> bool:
        if type(items) == list:
            return any(i in self.sprite for i in items)
        return items in self.sprite

    def activate_cleave(self):
        self.towers.remove(self)
        self.__class__.unlock(cleave=True)

    def distance(self, other) -> float:
        return (self.sprite.x - other.sprite.x) ** 2 + \
               (self.sprite.y - other.sprite.y) ** 2

    def __init__(self, x: int, y: int):
        super().__init__(x, y)      # allows multiple inheritance for tower
        self.sprite = self.spriter(x, y)
        self.name = type(self).__name__
        self.unlock()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.sprite = cls.spriter(*cls.position)
        if cls.locked:
            cls.sprite.opacity = 0
            if cls.shop:
                protein.locked_proteins[cls.__name__] = cls
            else:
                protein.combined_proteins[cls.__name__] = cls
        else:
            protein.shop_proteins[cls.__name__] = cls


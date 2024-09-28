import pyglet as py
from files import proteins as p


class enemy1:  # superclass
    def __init__(self, x, y, b1, g, j, s=0):
        self.vx, self.vy, self.camo = 0, 0, 0
        i = p.im(x=type(self).__dict__["x"], y=70, width=20, height=20)
        i.anchor_x, i.anchor_y, self.x, self.y = 10, 10, x, y
        self.sprite = py.sprite.Sprite(i, x, y, batch=b1, group=g)
        self.v, self.i, self.health = type(self).__dict__["v"], j, 2 + s
        self.damage, self.gold = self.v, self.v * 3
        self.base = type(self).__dict__["base"]  # magic method

    def run(self): pass


class six(enemy1):  # inheritance
    x, v, base = 200, 6, "5"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)
        self.damage = 6


class seven(enemy1):
    x, v, base = 120, 7, "6"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)
        self.damage = 7


class vaccinia(enemy1):
    x, v, range, base = 200, 4, 90, "0"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)
        self.circle = py.shapes.Circle(x, y, type(self).__dict__["range"], None, (255, 0, 255), b1, g)
        self.circle.opacity, self.health = 50, 5
        self.damage, self.gold = 8, 20

    def run(self): self.circle.position = (self.x, self.y)


class a(vaccinia):
    x, v, range, base = 0, 1, 30, "0"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)
        self.circle.opacity = 80
        self.circle.color, self.camo = (200, 200, 0), 1
        self.damage, self.gold = 2, 4


class b(a):
    x, v, range, base = 20, 2, 30, "a"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)
        self.circle.color, self.camo = (200, 200, 0), 1
        self.damage, self.gold = 4, 8


class c(a):
    x, v, range, base = 40, 3, 30, "b"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)
        self.circle.color, self.camo = (200, 200, 0), 1
        self.damage, self.gold = 5, 12


class d(a):
    x, v, range, base = 60, 4, 30, "c"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)
        self.circle.color, self.camo = (200, 200, 0), 1
        self.damage, self.gold = 6, 16


class e(a):
    x, v, range, base = 80, 5, 30, "d"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)
        self.circle.color, self.camo = (200, 200, 0), 1
        self.damage, self.gold = 7, 20


class f(a):
    x, v, range, base = 200, 6, 30, "e"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)
        self.circle.color, self.camo = (200, 200, 0), 1
        self.damage, self.gold = 8, 24


class k(a):
    x, v, range, base = 120, 7, 30, "f"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)
        self.circle.color, self.camo = (200, 200, 0), 1
        self.damage, self.gold = 9, 28


class s1(vaccinia):
    x, v, range, base = 200, 7, 35, "0"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)
        self.circle.opacity = 140
        self.circle.color, self.health = (255, 0, 0), 9
        self.damage, self.gold = 13, 30

    def run(self): self.circle.position, self.circle.color = (self.x, self.y), (28 * self.health, 0, 0)


class s2(s1):  # chained super/child classes
    x, v, range, base, = 200, 4, 35, "0"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)
        self.circle.color = (0, 0, 255)

    def run(self): self.circle.position, self.circle.color = (self.x, self.y), (0, 0, 28 * self.health)


class s3(s1):  # polymorphism
    x, v, range, base = 200, 1, 35, "0"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)
        self.circle.color = (0, 255, 0)

    def run(self): self.circle.position, self.circle.color = (self.x, self.y), (0, 28 * self.health, 0)


class fast(enemy1):
    x, v, base = 140, 9, "7"

    def __init__(self, x, y, b1, g, j, s=0):
        super().__init__(x, y, b1, g, j, s)


q, d1, v, n = {"1": enemy1}, -20, 0, -1
en = dict(q, **{str(i): type(str(i), (enemy1,), {}) for i in range(2, 6)})
for i in en.values():  # create some enemies using type()
    setattr(i, "x", (d1 := d1 + 20)), setattr(i, "v", (v := v + 1)), setattr(i, "base", (n := n + 1))
te = {"i": s3, "7": seven, "k": k, "l": fast}
en = dict(en, **{"6": six, "v": vaccinia, "a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": s1, "h": s2}, **te)
# final enemy dictionary

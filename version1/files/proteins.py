import pyglet as py, maths
import random as ra
from files import projectiles

temp7, proteins = open("text/info2"), {}
temp8, news = temp7.read(), [im := py.image.load("images/sprites.png").get_region]
temp8 = [i.strip().split(":") for i in temp8.strip().split(";")]
im1 = {i: float(j) for i, j in temp8}
bullets, towers, batch = [], [], py.graphics.Batch()


def new(t):  # image slice
    a, b, c, d = [int(j) for j in t["cut"][1:-1].split(",")]
    c = 35
    e = news[d](x=a, y=b, width=c, height=c)
    e.anchor_x, e.anchor_y = c // 2, c // 2
    return e, c


def dec1(a): return a


def dec3(a):  # custom decorator functions
    def mat(n, r):  # 2d linear transformation rotation matrix
        m1 = [[math.cos(r), -math.sin(r)], [math.sin(r), math.cos(r)]]
        return [n[0] * m1[j][0] + n[1] * m1[j][1] for j in range(2)]

    def inner(b, q, v):
        bullets.pop(-1)
        for j in range(0, 360, 30):
            h = mat([1, 1], j * math.pi / 180)  # use of matrices-rotate a point
            for k1 in h: k1 *= math.sqrt(h[0] ** 2 + h[1] ** 2) / k1
            bullets.append(projectiles.pro1(b.x, b.y, h[0], h[1], batch, b))
        a(b, q, v)

    return inner


def dec2(a):  # higher order function example-takes function as parameter
    def inner(b, q, v):  # slightly alter velocity components to create spread of projectiles
        bullets.append(projectiles.pro1(b.x, b.y, v[0] + 1, v[1], batch, b))
        bullets.append(projectiles.pro1(b.x, b.y, v[0], v[1] + 1, batch, b))
        a(b, q, v)

    return inner


class meta(type):  # metaclass-convert all class attributes to strings-normalise
    _instances = []  # protected member

    def __new__(mcs, name, bases,
                attrs):  # useful for any classes with attributes not defined in the text file (not already string type)
        t = lambda j: type(j).__name__  # filter out functions so they remain functional
        a = {q: str(j) for q, j in attrs.items() if t(j) != "function" and t(j) != "classmethod" and t(j) != "cell"}
        # if name in mcs._instances: raise Exception("Duplicate class creation not allowed")
        # else: mcs._instances.append(name)   #don't allow any repeated names for classes
        return super(meta, mcs).__new__(mcs, name, bases, dict(attrs,
                                                               **a))  # last parameter will override previous key values if there are duplicates


class C3b(metaclass=meta):  # this is the superclass
    @classmethod  # class method (not instance method)
    def add(cls, x, y):
        towers.append(cls(x, y))

    def special(self, q, v):
        self.temp(self, q, v)

    def downgrade(self, x):
        a = lambda y: math.ceil(y / 1.5)
        self.u_c[x] = a(self.u_c[x])
        self.sell -= self.u_c[x]
        self.u_p[x] -= 1
        return int(self.u_c[x] * 0.9)

    def upgrade(self, x):
        a = lambda y: math.floor(y * 1.5)
        self.sell += self.u_c[x]
        self.u_c[x] = a(self.u_c[x])
        self.u_p[x] += 1

    def __init__(self, x, y, c=0, d=(0, 0), co=(1, 1, 1, 1), w=0, r=0, co1=0, s=0):  # default values
        self.wait = [0, int((t := type(self).__dict__)["wait"]) + w]
        self.cost, self.range = int(t["cost"]), int(t["range"]) + r
        self.name, self.lvl = type(self).__name__, int(t["lvl"])  # magic methods
        self.sell, self.xy = self.cost if s == 0 else s, 0
        self.x, self.y, self.info, dec = x, y, t["info"], t["dec"]
        self.base, self.combine = t["base"], t["combine"]
        im2, self.width = new(t)
        self.sprite = py.sprite.Sprite(im2, x, y, batch=batch)
        # self.sprite.scale=im1[type(self).__name__]
        self.count, self.rot, self.b_v = c, 0, 3
        d1 = [int(j) for j in t["data"][1:-1].split(",")]
        self.data1, self.data2 = [d1[0] + d[0], d1[1] + d[1]]
        c = [float(j) for j in t["u_c"][1:-1].split(",")]
        self.u_c = [int(c[j] * co[j]) for j in range(4)]
        self.u_p = [0, 0, 0, 0] if co1 == 0 else co1

        @dec  # custom decorator
        def special(this, q, v):  # polymorphism with decorators, explained in the documented design
            this.rot = -q + 180 if v[0] < 0 else -q  # tower sprite rotation

        self.temp = special

    def attack(self, x, y, x1, y1, j):  # firing algorithm
        a, b = (y1 - y) / (x1 - x), j.vy - j.vx * (y1 - y) / (x1 - x)  # lots of algebra
        try:
            v1 = math.sqrt(4 * a ** 2 * b ** 2 - 4 * (a ** 2 + 1) * (b ** 2 - self.b_v ** 2))
        except ValueError:
            v1 = 0  # exact same maths equations used for the algorithm as in the documented design
        vx = (-2 * a * b + v1) / (2 * (a ** 2 + 1)) if (x - x1) > 0 else (-2 * a * b - v1) / (2 * (a ** 2 + 1))
        # vx1,vx2=(-2*a*b+v1)/(2*(a**2+1)),(-2*a*b-v1)/(2*(a**2+1))
        # vx=vx1 if (x1-x)/(j.vx-vx1)>0 else vx2
        # t=(x1-x)/(j.vx-vx)
        try:
            vy = math.sqrt(self.b_v ** 2 - vx ** 2) if (y1 - y) < 0 else -math.sqrt(self.b_v ** 2 - vx ** 2)
        except ValueError:
            vy = 0
        # vy=vy*-1 if y+j.vy*t<y1 else vy
        # vy=a*vx+b
        bullets.append(projectiles.pro1(x1, y1, vx, vy, batch, self))
        try:
            q = math.atan(vy / vx) * 180 / math.pi
        except ZeroDivisionError:
            q = 90
        self.special(q, [vx, vy])
        self.sprite.update(x1, y1, self.rot)

    def run(self, e, xy):
        self.wait[0], self.xy = self.wait[0] + 1 if 0 < self.wait[0] < self.wait[1] else 0, xy
        if self.wait[0] == 0:
            for j in e:
                if (j.x - self.x) ** 2 + (j.y - self.y) ** 2 < self.range ** 2:
                    if j.camo:  # dealing with camo enemies-if in range of a camo detecting tower then can still attack
                        for j1 in towers:  # camo detecting towers can also attack, if no towers then can't attack
                            if (n := type(j1).__name__) == "MBL" or n == "C3 Convertase" or n == "C5 Convertase":
                                if (j1.x - self.x) ** 2 + (j1.y - self.y) ** 2 < j1.range ** 2:
                                    self.attack(j.x, j.y, self.x, self.y, j)
                                    self.wait[0] = 1
                                    break
                    else:  # break to ensure only one attack-ensure efficiency
                        self.attack(j.x, j.y, self.x, self.y, j)
                        self.wait[0] = 1
                    if self.wait[0] == 1: break

    def difference(self, r1=0, d1=(0, 0), w1=0):  # carry upgrades across tower combination!!
        t = type(self).__dict__  # finds difference between current class/instance attribute
        d = [int(j) for j in t["data"][1:-1].split(",")]  # then can add onto combined class
        d = [self.data1 - d[0] + d1[0],
             self.data2 - d[1] + d1[1]]  # normalises values (difference between current and initial value)
        w = self.wait[1] - int(t["wait"]) + w1
        r = self.range - int(t["range"]) + r1
        co = [1.5 ** self.u_p[j] for j in range(4)]  # here it takes percentage instead of difference
        return [d, co, w, r, self.u_p,
                self.sell]  # passes the values to override default attributes of the next instance

    def revert(self):  # downgrade towers
        if self.lvl > 0:
            self.sell -= self.cost
            towers.append(proteins[self.base](self.x, self.y, self.count, *self.difference()))
        self.sprite.delete(), towers.pop(towers.index(self))
        return towers[-1] if self.lvl > 0 else None

    def __add__(self, a):  # combine towers-operator overloading
        towers.pop(towers.index(self)), self.sprite.delete()
        self.sell += int(proteins[a].__dict__["cost"])
        towers.append(proteins[a](self.x, self.y, self.count, *self.difference()))
        return towers[-1]


text, temp, a1 = open("text/info"), {}, {}  # read text file, lambda functions, string manipulation
z = lambda x: {h: {g[0]: g[x[0].index(h) + 1] for g in x[1:]} for h in x[0]}  # nested dictionary comprehension
z1 = lambda x: [[g.strip() for g in h.split(";")] for h in x.split("\n")]  # nested list comprehension
for i in [z(z1(j)) for j in text.read().split("\n.\n")]: temp = dict(temp, **i)
for m, j in temp.items():  # create classes, assign (class) attributes
    if m != "C3b":
        proteins[m] = type(m, (C3b,), {})  # use of type metaclass with 3 parameters-create new class
    else:
        proteins["C3b"] = C3b
    for k, l in j.items(): setattr(proteins[m], k, l)  # setattr


class Attack(C3b):  # custom classes not created using the text file
    range, cost, cut, base, combine, wait = 130, 95, (105, 125, 36, 0), "C5b-C8", "", 17
    lvl, data, u_c, info = 1, [100, 2], [20, 35, 15, 75], "."
    info1 = ""

    def __init__(self, x, y, c=0, d=(0, 0), co=(1, 1, 1, 1), w=0, r=0, co1=0, s=0):
        super().__init__(x, y, c, d, co, w, r, co1, s)
        if type(self).__name__ == "Attack":
            type(self).__name__ = "Attack Complex"
            self.cost1, self.name = 40, "Attack Complex"
        else:
            self.name, self.cost1 = type(self).__name__, int(40 * 1.5 ** int(self.lvl))

    def revert(self):  # polymorphism of revert function in the C3b class which this class inherits from
        self.sell -= self.cost
        a = "Attack Complex" if self.lvl == 2 else self.base if self.lvl == 1 else "Attack Complex (%s)" % (
                    int(self.lvl) - 2)
        towers.append(proteins[a](self.x, self.y, self.count, *self.difference(-6, (-20, -1), -1)))
        self.sprite.delete(), towers.pop(towers.index(self))
        return towers[-1] if int(self.lvl) > 0 else None

    def __add__(self, a):  # polymorphism of addition operator overload function in the C3b class
        towers.pop(towers.index(self)), self.sprite.delete()
        self.sell += int(self.cost1)
        a = "Attack Complex (%s)" % self.lvl
        towers.append(proteins[a](self.x, self.y, self.count, *self.difference(6, (20, 1), 1)))
        return towers[-1]


class Utilities(C3b):
    cut, wait, range, cost, base, combine, lvl = (210, 90, 36, 0), 34, 180, 115, "", "", 0
    data, u_c, info = [90, 2], [50, 50, 30, 90], "Manual firing, special abilities"
    info1 = ""

    def __init__(self, x, y, c=0, d=(0, 0), co=(1, 1, 1, 1), w=0, r=0, co1=0, s=0):
        super().__init__(x, y, c, d, co, w, r, co1, s)
        self.on, self.water = False, [0, 300]
        self.circle = py.shapes.Circle(self.x, self.y, self.range, None, (0, 255, 255))
        self.circle.opacity, self.tag = 0, []

    def new(self):
        r = int(self.range) / 2
        x, y = ra.randint(self.x - r, self.x + r), ra.randint(self.y - r, self.y + r)
        tex = "Temporary tower, meant to represent the C3a proteins, that after being cleaved from C3, " + \
              "would travel away from the pathogens to call for help from other immune cells."
        towers.append(type("temp C3a", (C3b,), {**C3b.__dict__, "info1": tex, "cost": 0})(x, y))
        setattr(towers[-1], "life", 500)  # dynamic class creating, uses composition, check utilities module
        towers[-1].sprite.opacity = 100
        self.tag.append(towers[-1])  # if this tower is sold, its C3a backup towers disappear also

    def run(self, e, xy):
        for j in self.tag:
            j.life -= 1
            if j.life < 1:
                j.sprite.delete()  # delete temp towers after time
                towers.pop(towers.index(j)), self.tag.pop(self.tag.index(j))
        if self.water[0] == 1:
            self.circle.opacity = 100
            for j in towers:
                if (j.x - self.x) ** 2 + (j.y - self.y) ** 2 < int(self.range) ** 2:
                    j.wait[1] -= 5
        if self.water[0] == self.water[1]:
            self.circle.opacity, self.water[0] = 0, 0
            for j in towers:
                if (j.x - self.x) ** 2 + (j.y - self.y) ** 2 < int(self.range) ** 2:
                    j.wait[1] += 5
        if int(self.water[0]) > 0: self.water[0] += 1
        if self.on:  # polymorphism-toggleable fire towards mouse option
            self.wait[0] = int(self.wait[0]) + 1 if 0 < int(self.wait[0]) < int(self.wait[1]) else 0
            d = math.sqrt((self.x - xy[0]) ** 2 + (self.y - xy[1]) ** 2)
            vx, vy = -10 * (self.x - xy[0]) / d, -10 * (self.y - xy[1]) / d
            if self.wait[0] == 0 and len(e) > 0:
                self.wait[0] = 1
                bullets.append(projectiles.pro1(self.x, self.y, vx, vy, batch, self))
            try:
                q = math.atan(vy / vx) * 180 / math.pi
            except ZeroDivisionError:
                q = 90
            self.special(q, [vx, vy])
            self.sprite.update(self.x, self.y, self.rot)


c1, proteins = open("text/info1"), {**proteins, "Attack Complex": Attack, "Utilities": Utilities}
c2, Attack.__name__ = c1.read(), "Attack Complex"
c1.close(), temp7.close(), text.close()
c3 = [i.strip().split(":") for i in c2.strip().split(";")]
for i in range(len(c3)):
    for k in range(c3[i][1].count("\n")):  # format info1 text file
        c3[i][1] = c3[i][1][:c3[i][1].index("\n")] + " " + c3[i][1][c3[i][1].index("\n") + 1:]
c4 = {i: j for i, j in c3}
for i in proteins.keys(): setattr(proteins[i], "info1", c4[i])  # add info1 attribute
for i in range(1, 17):  # create attack complex tower variations
    a1[b1] = type((b1 := "Attack Complex (%s)" % i), (Attack,), dict(Attack.__dict__, **{"lvl": i + 1}))
proteins = dict(proteins, **a1)  # final tower dictionary
for i in proteins.keys(): setattr(proteins[i], "dec", dec1)
setattr(proteins["C3bB"], "dec", dec2), setattr(proteins["C3bBb"], "dec", dec3)
# sets specific functions to certain towers-decorators-polymorphism (attacking method)
# class B(C3b):     #test class for duplicate class name creation handling
#   def __init__(self,x,y,c=0,d=(0,0),co=(1,1,1,1),w=0,r=0,co1=0,s=0):
#     super().__init__(x,y,c,d,co,w,r,co1,s)

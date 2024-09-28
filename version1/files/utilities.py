import pyglet as py
from files import proteins


class up:  # upgrade/view towers
    def __init__(self, b, g1, g2, g3, g4, t):
        q, self.antibody = [15, (255, 255, 255, 255), b, g2, False, 1, False, "left"], antibody()
        self.x, q1, xy1, xy2 = 0, [20, (255, 255, 0, 255), b, g2, True], [0, 22, 44, 66], [420, 360, 300, 240]
        self.rect1 = py.shapes.BorderedRectangle(0, 470, 199, 130, 5, (0, 0, 0), (200, 0, 200), b, g1)
        self.rect2 = py.shapes.BorderedRectangle(0, 0, 200, 470, 5, (70, 0, 0), (200, 0, 200), b, g1)
        self.c = py.shapes.Circle(0, 0, 1, colour=(100, 100, 100), batch=b, group=g1)
        self.rect1.opacity, self.rect2.opacity, self.c.opacity, self.on, self.data = 0, 0, 0, 0, ""
        self.xy, self.info, self.C3a = sum([[(i, j) for i in xy1] for j in xy2], []), 0, 0
        self.rects = [py.shapes.BorderedRectangle(0, y, 18, 12, 3, (255, 0, 0), (255, 255, 255), b, g1) for x, y in
                      self.xy]
        self.i_rect = py.shapes.BorderedRectangle(0, 0, 200, 470, 5, (70, 0, 0), (200, 0, 200), b, g3)
        self.i_rect.opacity = 0
        self.text1 = [t("", (800, 160), 15, (255, 255, 0, 255), b, g2, True, 0, True, "left"),
                      t("", (800, 172), 15, (255, 255, 255, 255), b, g2, False, 1, True, "left"),
                      t("", (800, 170), 14, (200, 0, 200, 200), b, g2, True, 1, True, "left"),
                      t("", (800, 448), 14, (255, 255, 255, 0), b, g4, False, 0, True, "left", 185),
                      t("", (800, 40), 20, (0, 0, 255, 235), b, g4, True),
                      t("", (800, 340), 14, (200, 0, 200, 200), b, g2, True, 1, True, "left"),
                      t("", (800, 280), 14, (200, 0, 200, 200), b, g2, True, 1, True, "left")]
        text = [["type", "", (800, 560), 20, (255, 255, 255, 255), b, g2],
                ["cost", "", (800, 530), 18, (255, 255, 255, 255), b, g2],
                ["count", "", (800, 500), 18, (255, 255, 255, 255), b, g2],
                ["sell", "", (800, 80), 20, (255, 255, 0, 255), b, g2, True],
                ["value", "", (800, 195), 20, (255, 255, 255, 255), b, g2],
                ["r", "", (0, 440), *q], ["s", "", (0, 380), *q], ["l", "", (0, 320), *q], ["d", "", (0, 260), *q],
                ["11", "", (0, 420), *q], ["22", "", (0, 360), *q], ["33", "", (0, 300), *q], ["44", "", (0, 240), *q],
                ["1", "", (0, 415), *q1], ["2", "", (0, 355), *q1], ["3", "", (0, 295), *q1], ["4", "", (0, 235), *q1],
                ["111", "", (0, 440), *q1], ["222", "", (0, 380), *q1], ["333", "", (0, 320), *q1],
                ["444", "", (0, 260), *q1]]
        self.text, self.ut = {i[0]: t(*i[1:]) for i in text}, 0
        self.n, a = ("", 0), [[0, 22, 44, 66, 88, 110, 132, 154], [150, 130]]
        self.a1 = sum([[(i, j) for i in a[0]] for j in a[1]], [])
        self.a_rects = [py.shapes.BorderedRectangle(0, y, 18, 12, 3, (255, 0, 0), (255, 255, 255), b, g1) for x, y in
                        self.a1]
        for i in self.rects + self.a_rects: i.opacity = 0

    def special(self, n):  # C3 Convertase/Attack Complex special upgrade functionality
        if n == "C3bBbp":
            self.text1[0].text, self.n = "Activate C3 Convertase (£80)", ("C3 Convertase", 80)
        elif n == "C5b-C8":  # other behaviour (buttons/special abilities/upgrades) manually created
            self.text1[0].text, self.n = "Activate Attack Complex (£95)", ("Attack Complex", 95)

    def special1(self, x, y, p, u, g):
        if self.n[0] == "C5" and left(x, y, self.text1[2]):
            self.text1[2].font_size = 16
            if g.stats["gold"] >= self.n[1] and p.a():
                u("gold", -self.n[1]), self.antibody.load(x, y), self.end()
        else:
            self.text1[2].font_size = 14
        if self.ut:
            if left(x, y, self.text1[6]):
                self.text1[6].font_size = 16
                if g.stats["lives"] > 1 and p.a() and self.data.water[0] == 0:
                    u("lives", -1), self.up()
                    self.data.water[0] = 1
            else:
                self.text1[6].font_size = 14
            if left(x, y, self.text1[5]):
                self.text1[5].font_size = 16
                if g.stats["gold"] >= 40 and p.a() and len(self.data.tag) < 4:
                    u("gold", -40), self.data.new()
            else:
                self.text1[5].font_size = 14
            if left(x, y, self.text1[2]):
                self.text1[2].font_size = 16
                if p.a(): self.data.on = not self.data.on
            else:
                self.text1[2].font_size = 14
        elif self.n[0] != "":  # attack complex-extra bars-C9's
            if left(x, y, self.text1[0]):
                self.text1[0].font_size = 18
                if g.stats["gold"] >= self.n[1] and p.a():
                    temp = self.data + self.n[0]
                    temp.sprite.update(self.data.x, self.data.y, self.data.rot), u("gold", -self.n[1])
                    self.data, self.n, self.text1[0].text = temp, ("", 0), ""
                    self.set(self.data)
            else:
                self.text1[0].font_size = 15

    def up(self):
        self.text["r"].text = "Attack range: %s" % self.data.range
        self.text["s"].text = "Reload time: %s" % self.data.wait[1]
        if not self.ut:
            self.text["l"].text = "Bullet lifespan: %s" % (self.data.data1 // 10)
            self.text["d"].text = "Bullet damage: %s" % self.data.data2

    def set(self, i):  # initialise text
        for j in self.a_rects: j.opacity = 0
        for j in self.text1 + list(self.text.values()): j.text = ""
        self.on, self.data, self.c.opacity, self.ut, self.C3a = True, i, 100, False, 0
        self.rect1.opacity, self.rect2.opacity, self.text1[4].text = 255, 255, "Info"
        self.c.radius, self.c.position, self.c.color = i.range, (i.x, i.y), (100, 100, 100)
        self.text["type"].text = "Tower: %s" % i.name
        self.text1[3].text = type(i).info1
        if i.name == "C3b":
            self.text1[1].text = "(can also combine with C3 Convertase)"
        elif i.name == "Utilities":
            self.ut = True
            self.text1[2].text = "Toggle manual       firing"
            self.text1[5].text = "Temporary C3a    backup (£40)"
            self.text1[6].text = "Temporary water concentration    increase (1 life)"
        elif i.name == "C3 Convertase" or i.name == "C5 Convertase" or i.name == "MBL" \
                or i.name == "C1 Complex (1)" or i.name == "C1 Complex (2)" or i.name == "MBL Complex":
            self.text["type"].font_size, self.c.color = 15, (200, 0, 200)
            if i.name == "C3 Convertase":
                self.text1[1].text = "(allows camo enemies to be seen by all in its range)"
            elif i.name == "MBL":
                self.text1[1].text = "(slows enemies and allows camo enemies to be seen)"
            elif i.name == "C5 Convertase":
                self.text1[2].text, self.n = "Special Ability (£40) -Summon Antibody ", ("C5", 40)
        elif type(i).__name__ == "Attack Complex" or issubclass(type(i), proteins.Attack):
            self.text["type"].font_size, self.text1[1].text = 12, "C9's: %s" % (i.lvl - 1)
            for j in self.a_rects: j.opacity = 255
            for j in range(i.lvl - 1): self.a_rects[j].colour = (0, 50, 255)
            for j in range(16): self.a_rects[j].x = self.x + 10 + self.a1[j][0]
        else:
            self.c.color, self.text1[2].text = (100, 100, 100), ""
            self.text["type"].font_size, self.text1[1].text = 20, ""
            for j in self.a_rects: j.opacity = 0
        self.up(), self.special(i.name)
        self.text["sell"].text = "Sell" if i.lvl < 1 else "Downgrade"
        if i.lvl > 0:
            self.text["cost"].text = "Downgrade cost: £%s" % int(i.cost * 0.9)
            self.text["cost"].font_size = 16
        else:
            self.text["cost"].text = "Sell cost: £%s" % int(i.sell * 0.9)
            self.text["cost"].font_size = 18
        self.text["value"].text = "Total value: £" + str(int(i.sell * 0.9))
        self.text["11"].text, self.text["22"].text = "£%s" % i.u_c[0], "£%s" % i.u_c[1]
        if not self.ut: self.text["33"].text, self.text["44"].text = "£%s" % i.u_c[2], "£%s" % i.u_c[3]
        self.text["1"].text, self.text["2"].text = "(+)", "(+)"
        if not self.ut: self.text["3"].text, self.text["4"].text = "(+)", "(+)"
        self.text["111"].text, self.text["222"].text = "(-)", "(-)"
        if not self.ut: self.text["333"].text, self.text["444"].text = "(-)", "(-)"
        for j in self.rects: j.color, j.opacity = (255, 0, 0), 255
        for j in range(4):
            for k in range(i.u_p[j]): self.rects[4 * j + k].colour = (0, 255, 0)
        if self.ut:
            for j in range(8, 16): self.rects[j].opacity = 0
        if type(i).__name__ == "temp C3a":  # special tower-no upgrades, only info, can't toggle
            self.C3a, self.info = True, True
            self.text1[4].colour = (*self.text1[4].colour[:3], 0)
            self.text1[3].colour = (255, 255, 255, 255)
            self.i_rect.opacity = 255

    def start(self, i):  # set initial values/colours/opacities/positions for text/shape primitives
        self.text["count"].colour = (255, 255, 255, 255)
        for j in self.rects: j.opacity = 255
        for j in list(self.text.values())[5:9] + self.text1: j.x = 710 if i.x < 350 else 10
        for j in list(self.text.values())[:5] + [self.text1[4]]: j.x = 800 if i.x < 350 else 100
        for j in list(self.text.values())[9:13]: j.x = 810 if i.x < 350 else 110
        for j in list(self.text.values())[13:17]: j.x = 875 if i.x < 350 else 175
        for j in list(self.text.values())[17:]: j.x = 880 if i.x < 350 else 180
        for j in range(16): self.rects[j].x = 710 + self.xy[j][0] if i.x < 350 else 10 + self.xy[j][0]
        self.rect1.x, self.rect2.x, self.x, self.i_rect.x = (x := 700 if i.x < 350 else 0), x, x, x

    def upgrade(self, x, y, p, u, g):  # upgrade stats for towers (damage/bullet lifespan/range/speed)
        for i in list(self.text.keys())[13:17]:
            if active(x, y, self.text[i]):
                if g.stats["gold"] >= self.data.u_c[int(i) - 1] and self.data.u_p[int(i) - 1] < 4 and p.a():
                    if i == "1":
                        setattr(self.data, "range", self.data.range + 5)
                        self.c.radius = self.data.range
                    elif i == "2":
                        setattr(self.data, "wait", [self.data.wait[0], self.data.wait[1] - 2])
                    elif i == "3" and not self.ut:
                        setattr(self.data, "data1", int(self.data.data1 * 1.2))
                    elif i == "4" and not self.ut:
                        setattr(self.data, "data2", self.data.data2 + 1)
                    u("gold", -self.data.u_c[int(i) - 1]), self.data.upgrade(int(i) - 1), self.up()
                    self.text[i * 2].text = "£" + str(self.data.u_c[int(i) - 1])
                    self.rects[4 * (int(i) - 1) + self.data.u_p[int(i) - 1] - 1].colour = (
                    0, 255, 0)  # value indicates index
                    self.text["value"].text = "Total value: £%s" % int(self.data.sell * 0.9)
                    if self.data.u_p[int(i) - 1] == 4: self.text[i * 2].text = "Max"  # if upgraded 4 times
                    if self.data.lvl == 0: self.text["cost"].text = "Sell cost: £%s" % int(self.data.sell * 0.9)
                self.text[i].font_size = 24
            else:
                self.text[i].font_size = 20
            if active(x, y, self.text[i * 3]):  # downgrades also
                if 0 < self.data.u_p[int(i) - 1] and p.a():
                    if i == "1":
                        setattr(self.data, "range", self.data.range - 5)
                        self.c.radius = self.data.range
                    elif i == "2":
                        setattr(self.data, "wait", [self.data.wait[0], self.data.wait[1] + 2])
                    elif i == "3" and not self.ut:
                        setattr(self.data, "data1", int(self.data.data1 / 1.2))
                    elif i == "4" and not self.ut:
                        setattr(self.data, "data2", self.data.data2 - 1)
                    u("gold", self.data.downgrade(int(i) - 1)), self.up()
                    self.text[i * 2].text = "£" + str(self.data.u_c[int(i) - 1])
                    self.rects[4 * (int(i) - 1) + self.data.u_p[int(i) - 1]].colour = (255, 0, 0)
                    self.text["value"].text = "Total value: £%s" % int(self.data.sell * 0.9)
                    if self.data.lvl == 0: self.text["cost"].text = "Sell cost: £%s" % int(self.data.sell * 0.9)
                self.text[i * 3].font_size = 24
            else:
                self.text[i * 3].font_size = 20

    def update(self, x, y, p, u, g):  # info/sell buttons/any text regularly updated
        if not self.info: self.upgrade(x, y, p, u, g), self.special1(x, y, p, u, g)
        if "Pop count: %s" % self.data.count != self.text["count"].text:
            self.text["count"].text = "Pop count: %s" % self.data.count
        if type(self.data).__name__ == "temp C3a":
            if self.data.life < 1: self.end()
        if active(x, y, self.text1[4]) and not self.C3a:
            self.text1[4].font_size = 24
            if p.a():
                if not self.info:
                    self.text1[3].colour = (255, 255, 255, 255)
                    self.i_rect.opacity = 255
                else:
                    self.text1[3].colour = (255, 255, 255, 0)
                    self.i_rect.opacity = 0
                self.info = not self.info
        else:
            self.text1[4].font_size = 20
        if not self.info and active(x, y, self.text["sell"]):
            self.text["sell"].font_size = 24
            if p.a():
                if self.ut:  # composition,delete temp C3a's if parent (utilities) tower sold
                    for i in self.data.tag:
                        i.sprite.delete(), proteins.towers.pop(proteins.towers.index(i))
                u("gold", int(0.9 * self.data.cost))
                t, self.n, self.text1[0].text = self.data.revert(), ("", 0), ""
                if type(t).__name__ == "Attack Complex" or issubclass(type(t), proteins.Attack):
                    for j in self.a_rects: j.color = (255, 0, 0)
                if t is None:
                    self.end()
                else:
                    self.set(t), t.sprite.update(self.data.x, self.data.y, self.data.rot)
        else:
            self.text["sell"].font_size = 20

    def end(self):  # reset values
        self.text1[4].colour = (*self.text1[4].colour[:3], 255)
        self.n, self.i_rect.opacity, self.text1[3].colour = ("", 0), 0, (255, 255, 255, 0)
        for j in self.rects + self.a_rects: j.color, j.opacity = (255, 0, 0), 0
        self.rect1.opacity, self.rect2.opacity, self.c.opacity = 0, 0, 0
        for i in list(self.text.values()) + self.text1: i.text = ""
        self.on, self.x, self.rect1.x, self.C3a = False, 0, 0, 0
        self.text["count"].colour, self.info = (0, 0, 0, 0), 0


class scroll:  # scroll bar
    def __init__(self, b2, g2):
        self.s = py.shapes.BorderedRectangle(854, 360, 38, 103, 6, (100, 255, 100), (0, 0, 0), b2, g2)
        self.on, self.sy = False, 400

    def slide(self, x, y, p, dy, g):
        if p.a() and 853 < x < 893 and self.s.y < y < self.s.y + 85 and not self.on:
            self.on, self.sy = True, y
        elif not p.p:
            self.on = False
        if self.on:
            if self.s.y > 360 and dy > 0 or self.s.y < 5 and dy < 0:
                a = 0
            else:
                a = s - 5 if (d := self.sy - y) > (s := self.s.y) - 5 else d if d > s - 360 else s - 360
            self.s.y, self.sy = self.s.y - a, y
            for i in g.grid: i[1] += a * 1.3
            for i in g.rect + g.red + g.side: i.y += a * 1.3


class click:  # place tower-container for data while tower is being dragged
    def __init__(self, b, g, im):
        self.on, self.im = 0, im(x=0, y=0, width=1, height=1)
        self.sp = py.sprite.Sprite(self.im, -1, -1, batch=b, group=g)
        self.c = py.shapes.Circle(0, 0, 1, None, (0, 0, 0), b, g)
        self.c.opacity, self.data, self.pos = 0, [], (0, 0)

    def start(self, data):
        self.sp.update(*data[:2]), self.update_c((255, 0, 0))
        self.sp.image, self.c.radius = data[2], int(data[5])
        self.on, self.c.opacity, self.data = True, 100, data
        self.c.x, self.c.y = data[:2]

    def update_c(self, c, i=0):
        self.c.color = c
        if i != 0: self.data.append(i)

    def update(self, x, y):
        self.sp.update(x, y)
        self.c.x, self.c.y = x, y

    def end(self):
        self.c.opacity, self.on, self.sp.image = 0, 0, self.im
        self.sp.update(-1, -1)


def active(x, y, t):
    a, b = t.content_width, t.content_height
    if t.x - a / 2 < x < t.x + a / 2 and t.y < y < t.y + b / 2:
        return True


def left(x, y, t):
    a, b = t.content_width, t.content_height
    if t.x < x < t.x + a and t.y - b / 2 < y < t.y + b / 2:
        return True


def default(x, a, b):
    a[x].colour = b[x].colour
    a[x].font_size = b[x].font_size


class antibody:  # antibody special ability
    def __init__(self):
        self.circle = py.shapes.Circle(0, 0, 80, None, (100, 0, 100))
        self.circle.opacity, self.on = 80, 0

    def load(self, x, y):
        self.on, self.circle.position, self.circle.opacity = 1, (x, y), 80

    def end(self, q):
        for i in q.active:  # when click-deals damage to any enemies in range
            if (self.circle.x - i.x) ** 2 + (self.circle.y - i.y) ** 2 < 6400:
                i.health -= 7
        self.circle.opacity, self.on = 0, 0

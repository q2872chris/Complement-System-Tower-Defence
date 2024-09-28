import pyglet as py
from pyglet import shapes as sh, sprite as spr
from files import proteins as pr, utilities as ut

b1, g, b3, lives = py.graphics.Batch(), py.graphics.OrderedGroup, py.graphics.Batch(), 0
g1, g2, g3, g4, font, pr1 = g(0), g(1), g(2), g(3), "Times New Roman", pr.proteins  # batched/grouped rendering
ln, b2 = [[0, 598, 900, 598], [1, 0, 1, 600], [900, 0, 900, 600], [0, 0, 900, 0]], py.graphics.Batch()
pr2 = ["C3b", "C3a", "B", "D", "Ba", "P", "C5b", "C5a", "C6", "C7", "C8", "C9", "MBL", "Utilities",
       "C1q", "C1r", "C1s", "C4b", "C4a", "C2b", "C2a", "MASP-1", "MASP-2"]  # placeable towers in order
unlock = {("C3bB", 3): ["D"], ("C3bBb", 4): ["Ba", "P"], ("C5 Convertase", 6): ["C5b", "C5a"], ("C5b", 8): ["C6"],
          ("C5bC6", 9): ["C7"], ("C5b-C7", 10): ["C8"], ("C5b-C8", 11): ["C9", "MBL", "Utilities", "C1q"],
          ("C1q", 15): ["C1r"], ("C1 Complex (1)", 16): ["C1s"], ("C1 Complex (2)", 17): ["C4b", "C4a"],
          ("C4b", 19): ["C2b", "C2a", "MASP-1"], ("MASP-1", 22): ["MASP-2"]}  # unlock new towers dictionary ^


# [x,y,im,name,cost,range,radius,info,class,width]#grid data
# [0,1, 2,   3,   4,    5,     6,   7,    8,    9]
def t1(a, x, s, c, d=None, g5=None, q=False, i=0, m=False, c_x="centre", w=190):
    return py.text.Label(a, font, s, bold=q, italic=i, colour=c, x=x[0], y=x[1], width=w,
                         anchor_x=c_x, multiline=m, batch=d, group=g5)


class game:
    def fill(self):
        for i in range(3, self.filled):  # fill automatically if load game
            self.side.append(spr.Sprite((n := self.grid[i])[2], n[0] + 38, n[1] + 38, batch=b1, group=g3))

    def __init__(self):
        self.line = sh.Line(0, 0, 900, 0, 5, (200, 0, 200), b2, g2)
        self.p_rect = py.shapes.Rectangle(0, 0, 900, 600, (120, 120, 120), b3, g3)
        self.filled, self.rects, self.red, self.rect, self.p_rect.opacity = (f := 3), [], [], [], 0
        self.b = sum([[[i, j] for i in [700, 775]] for j in [394 - 75 * i for i in range(12)]], [])
        i = [[(ne := pr.new(i.__dict__))[0], i.__name__, i.cost, i.range, 35, i.info, i, ne[1]] for i in
             [pr1[j] for j in pr2]]
        self.grid, self.scroll = [self.b[j] + i[j] for j in range(len(pr2))], ut.scroll(b2,
                                                                                        g2)  # tower data-take from protein tower class attributes
        self.rects.append(sh.BorderedRectangle(700, 470, 199, 130, 5, (0, 0, 0), (200, 0, 200), b2,
                                               g3))  # generate rectangle primitives
        self.rects.append(sh.BorderedRectangle(700, 0, 200, 470, 5, (70, 0, 0), (200, 0, 200), b1, g2))
        self.side = [spr.Sprite(i[2], i[0] + 38, i[1] + 38, batch=b2, group=g1) for i in self.grid[:f]]  # tower sprites
        for i in ln: self.rects.append(sh.Line(*i, 5, (200, 0, 200), b1, g4))
        for i, j in self.b[:30]:  # transparent rectangles for if not enough money for a tower
            self.rect.append(sh.BorderedRectangle(i, j, 75, 75, 5, (70, 0, 0), (200, 0, 200), b1, g2))
            self.red.append(sh.Rectangle(i + 2, j + 2, 71, 71, (255, 0, 0), b1, g4))
            self.red[-1].opacity = 0
        self.stats, self.click = {"gold": 800, "lives": 80, "round": 0}, ut.click(b2, g2, pr.im)
        globals()["lives"] = self.stats[
            "lives"]  # set a static initial value for the lives value but allows it to be set in the dictionary
        self.strings = {"gold": "Amino acids: %s", "lives": "Damage taken: %s/" + str(self.stats["lives"]),
                        "round": "Wave: %s"}
        text = [["type", "C3b", (800, 550), 30, (255, 255, 255, 255), b2, g4],
                # displayable text data
                ["cost", "£%s" % pr1["C3b"].cost, (800, 510), 25, (255, 255, 0, 255), b2, g4],
                ["flash", "", (445, 350), 70, (255, 255, 0, 0), b3, g4],
                ["gold", "Amino acids: %s" % self.stats["gold"], (590, 545), 20, (255, 255, 255, 255), b2, g1],
                ["lives", "Damage taken: %s/%s" % (0, self.stats["lives"]), (580, 570), 20, (255, 255, 255, 255), b2,
                 g1],
                ["round", "Wave: %s" % self.stats["round"], (640, 520), 20, (255, 255, 255, 255), b2, g1],
                ["info", "info", (660, 495), 19, (0, 0, 0, 255), b2, g1, True, 4],
                ["play", "play", (660, 470), 19, (0, 0, 0, 255), b2, g1, True, 4],
                ["back", "settings?", (640, 445), 19, (0, 0, 0, 255), b2, g1, True, 4],
                ["auto", "auto", (660, 420), 19, (0, 0, 0, 255), b2, g1, True, 4],
                ["info1", "", (800, 510), 18, (255, 255, 255, 255), b2, g4, False, 0, True],
                ["pause", "Paused", (400, 420), 80, (0, 0, 0, 0), b3, g4],
                ["resume", "Resume", (400, 300), 50, (200, 200, 0, 0), b3, g4],
                ["title", "Title screen", (400, 200), 50, (200, 200, 0, 0), b3, g4]]
        self.text, self.up = {i[0]: t1(*i[1:]) for i in text}, ut.up(b3, g1, g2, g3, g4,
                                                                     t1)  # convert list of data to dictionary of text labels via dictionary comprehension
        self.fade, self.info, self.pause, self.auto = [-1, 0], 0, False, 0
        self.queue = ["C3b Unlocked", "C3a Unlocked", "B Unlocked"]

    def view(self, x, y, p, q):
        if self.up.antibody.on:  # antibody special ability
            self.up.antibody.circle.position = (x, y)
            if p.a(): self.up.antibody.end(q)
        for i in pr.towers:  # upgrade section
            if i.x - 18 < x < i.x + 18 and i.y - 18 < y < i.y + 18:
                if (p.p and self.up.on) or p.a():
                    if not self.up.on:
                        self.up.start(i), self.up.set(i)  # initialise tower panel
                    else:
                        self.up.set(i)  # new tower panel
                    break
        else:
            if p.p and ((x < 700 and self.up.x == 700) or (x > 200 and self.up.x == 0)) and self.up.on:
                self.up.end()  # finished tower panel
        if self.up.on: self.up.update(x, y, p, self.update, self)  # run current tower panel

    def mini(self, j):  # utilises queue more-unlocking announcements
        if (j, self.filled) in unlock.keys():
            for i in unlock[(j, self.filled)]:
                self.filled = (f := self.filled) + 1  # new sprite/tower unlocked
                self.side.append(spr.Sprite((n := self.grid[f])[2], n[0] + 38, n[1] + 38, batch=b1, group=g3))
                self.queue.append(i + " unlocked")  # text to go to text displaying queue (list)

    def drag(self, q, x, y, p):
        if p.p and self.click.on:
            self.click.update(x, y), self.update("info1", "")
            if self.click.c.color != [0, 0, 255]:
                self.update("type", self.click.data[3]), self.update("cost", "£" + self.click.data[4])
            if x < 20 or x > 680 or y < 20 or y > 580:
                self.click.update_c((255, 0, 0))
            elif self.click.c.color != [0, 255, 0]:
                self.click.update_c((0, 255, 0))
            for a, b, c, d, e, f in q.vecs:  # check for collisions with the track-further vector maths
                l = (c * ((x1 := self.click.c.x) - a) + d * ((y1 := self.click.c.y) - b)) / (c ** 2 + d ** 2)
                if min(a, e) <= a + l * c <= max(a, e) and min(b, f) <= b + l * d <= max(b, f):
                    if (x1 - a - l * c) ** 2 + (y1 - b - l * d) ** 2 < (15 + self.click.data[9] / 2) ** 2:
                        self.click.update_c((255, 0, 0))  # check track vertices also, change colour to red if collision
                elif (x1 - a) ** 2 + (y1 - b) ** 2 < (15 + self.click.data[9] / 2) ** 2:
                    self.click.update_c((255, 0, 0))
            for i in pr.towers:  # check if the new tower is being placed onto a compatible placed tower
                self.text["type"].font_size = 30
                if i.x - 35 < x < i.x + 35 and i.y - 35 < y < i.y + 35 and not type(i).__name__ == "temp C3a":
                    if type(i).__name__ == self.click.data[8].base or \
                            (self.click.data[8].__name__ == "C9" and issubclass(type(i), pr.Attack)):
                        self.click.update_c((0, 0, 255), i)  # change range colour from green to blue if intersection
                        if self.click.data[8].__name__ == "C9":
                            self.text["type"].font_size = 18
                            self.update("cost", "£" + str(i.cost1))
                            self.update("type", "Attack complex (%s)" % i.lvl)
                            self.click.data.insert(-1, i.cost1)
                            if self.stats["gold"] < i.cost1: self.click.update_c((255, 0, 0))
                        else:
                            self.click.data.insert(-1, pr1[self.click.data[8].combine].cost)
                            self.update("cost", "£" + pr1[self.click.data[8].combine].cost)
                            self.update("type", n := self.click.data[8].combine)
                            if n == "C3 Convertase" or n == "C5 Convertase" \
                                    or n == "C1 Complex (1)" or n == "C1 Complex (2)" or n == "MBL Complex":
                                self.text["type"].font_size = 23  # manually alter font size for long names
                            if self.stats["gold"] < int(pr1[self.click.data[8].combine].cost):
                                self.click.update_c((255, 0, 0))
                    else:
                        self.click.update_c((255, 0, 0))
        for i in self.grid[:self.filled]:  # check for if hover over tower
            if self.red[self.grid.index(i)].opacity == 0 and int(i[4]) > self.stats["gold"]:
                self.red[self.grid.index(i)].opacity = 100  # red transparent rectangle
            elif self.red[self.grid.index(i)].opacity == 100 and int(i[4]) <= self.stats["gold"]:
                self.red[self.grid.index(i)].opacity = 0
            if i[0] + 10 < x < i[0] + 65 and i[1] + 10 < y < i[1] + 65 and not self.click.on and y < 470:
                self.text["type"].font_size = 30
                if p.a() and int(i[4]) <= self.stats["gold"] and not self.scroll.on:
                    if self.up.rect1.x == 0:
                        self.click.start(i[:]), self.up.end()  # pick up new tower
                else:
                    self.update("type", i[3])
                    if self.info:
                        self.update("cost", ""), self.update("info1", i[7])
                    else:
                        self.update("cost", "£%s" % i[4]), self.update("info1", "")
        if not p.p and self.click.on:  # create new tower
            self.click.end()
            if self.info: self.update("info1", self.click.data[7]), self.update("cost", "")
            if self.click.c.color == [0, 255, 0]:
                self.update("gold", -int(self.click.data[4]))
                self.click.data[8].add(x, y), self.mini(self.click.data[3])  # class method usage
            elif self.click.c.color == [0, 0, 255]:
                self.update("gold", -int(self.click.data[-2]))
                temp = self.click.data[-1] + self.click.data[8].combine  # operator overloaded function usage
                self.mini(pr1[self.click.data[3]].combine)
                temp.sprite.update(temp.x, temp.y, self.click.data[-1].rot)  # rotate new tower sprite

    def active(self, x, y, q, p):  # buttons-play/auto/title screen (pause)/tower info (toggleable)
        for i in list(self.text.keys())[6:11]:
            if ut.active(x, y, (t := self.text[i])):
                self.text[i].font_size, self.text[i].colour = 21, (150, 220, 220, 255)
                if i == "info" and p.a():
                    self.info = not self.info
                elif i == "auto" and p.a():
                    self.auto = not self.auto
                elif i == "play" and p.a() and not q.r_pause:
                    q.pause, q.r_pause = 1, 1
                    self.update((f := "round"), 1), self.queue.append("Wave %s" % self.stats[f])
                elif i == "back" and p.a():
                    self.text["flash"].text = ""
                    self.pause, self.p_rect.opacity = True, 100
                    self.text["pause"].colour = (0, 0, 0, 100)
                    self.text["resume"].colour = (220, 220, 0, 255)
                    self.text["title"].colour = (220, 220, 0, 255)
                if i == "auto" and self.auto:
                    t.color = (50, 50, 255, 255)
                elif i == "play" and q.r_pause:
                    t.color = (50, 50, 255, 255)
                elif i == "info" and self.info:
                    self.text[i].colour = (0, 255, 80, 255)
            else:
                self.text[i].font_size, self.text[i].colour = 19, (100, 100, 200, 200)
                if i == "play" and q.r_pause:
                    self.text[i].colour = (60, 60, 255, 255)
                elif i == "auto" and self.auto:
                    self.text[i].colour = (60, 60, 255, 255)
                elif i == "info" and self.info:
                    self.text[i].colour = (0, 255, 100, 255)

    def run(self, win, q, dt):  # runs the other functions
        if len(self.queue) > 0 > self.fade[0] and not self.pause:
            self.fade, self.text["flash"].text = [0, True], self.queue[0]
            self.queue.pop(0)
        if self.fade[0] > -1:  # fade in/out text displaying queue system
            self.text["flash"].colour = (255, 255, 0, self.fade[0])
            self.fade = [f[0] + 4, 1] if (f := self.fade)[1] and f[0] < 252 else [f[0] - 4, 0]
        if not self.pause:
            self.drag(q, *win.xy, win.p)
        else:
            self.back(*win.xy, win)  # boolean logic-only run certain functions-if paused or not/etc
        if not self.click.on and not self.scroll.on and not self.pause:
            self.active(*win.xy, q, win.p)
        if not self.click.on and not self.pause:
            self.view(*win.xy, win.p, q), self.scroll.slide(*win.xy, win.p, win.dxy[1], self)
        if not self.pause:
            for i in pr.towers: i.run(q.active, win.xy)
            for j in pr.bullets:  # bullet movement,bullet/enemy collisions
                j.x, j.y = j.x + j.vx * dt * 50, j.y + j.vy * dt * 50
                j.rect.x, j.rect.y = j.x, j.y
                j.count += 1
                if j.x < 0 or j.x > 700 or j.y < 0 or j.y > 600 or j.count > j.life:
                    pr.bullets.pop(pr.bullets.index(j))
                    continue
                for i in q.active:
                    if i.x - 10 < j.x + 2 < i.x + 10 and i.y - 10 < j.y + 2 < i.y + 10:
                        i.health, j.p.count = i.health - j.damage, j.p.count + 1
                        pr.bullets.pop(pr.bullets.index(j))
                        break

    def back(self, x, y, win, c=0):  # pause/resume/load screen
        if ut.active(x, y, self.text["resume"]):
            self.text["resume"].font_size = 60
            if win.p.a(): c, self.pause = True, 0
        else:
            self.text["resume"].font_size = 50
        if ut.active(x, y, self.text["title"]):
            self.text["title"].font_size = 60
            if win.p.a(): c, win.pause, self.pause = True, True, 0
        else:
            self.text["title"].font_size = 50
        if c:
            self.p_rect.opacity = 0
            for i in list(self.text.values())[11:14]:
                i.color, i.font_size = (0, 0, 0, 0), 80 if i.text == "Paused" else 50

    def update(self, q, q1):  # text update function
        if type(q1) == int:
            self.stats[q] = self.stats[q] + q1  # uses the static initial lives value
            if q == "lives":
                self.text[q].text = self.strings[q] % (lives - self.stats[q])
            else:
                self.text[q].text = self.strings[q] % self.stats[q]
        else:
            self.text[q].text = q1



import pyglet as py
import sqlite3
import random as ra
from pyglet.window import key
from files import game, screens, queue, proteins, utilities as ut, enemies as e

g, q, s = game.game(), queue.queue(), screens.screen()
ba, it, batch2 = py.graphics.Batch(), [], py.graphics.Batch()  # sql table creation statements
players = """create table if not exists players(
             ID string primary key,round integer not null,gold integer not null,
             lives integer not null,speed integer not null,fill integer not null,
             place integer not null)"""
towers = """create table if not exists towers(
             ID string not null,x integer not null,y integer not null,type string not null,
             count integer not null,co string not null,d string not null,w integer not null,
             r integer not null,co1 string not null,sell integer not null,
             foreign key (ID) references players(ID) on delete cascade)"""


class window(py.window.Window):  # working foreign key relationship
    def __init__(self, *args, **kwargs):
        cursor = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
        super().__init__(*args, **kwargs), self.set_mouse_cursor(cursor)
        self.keys = key.KeyStateHandler(), py.clock.schedule_interval(self.update, 0.01)
        self.xy, self.dxy, self.pause, self.end, self.save, self.load2 = [0, 0], [0, 0], 1, 0, 0, ""
        it.append(py.shapes.BorderedRectangle(0, 0, 900, 600, 6, (0, 180, 255), (0, 150, 0), ba, game.g1))
        self.push_handlers(self.keys), self.set_location(200, 50)
        self.text, self.enter, self.cur, self.con, self.d, self.load = "", 0, 0, 0, 0, 0
        self.show_scores, self.scores, self.save1, self.load1 = 0, [], 0, 0
        self.text1 = [game.t1("Back", (450, 50), 45, (210, 210, 0, 0), ba, game.g2),
                      game.t1("Not valid", (450, 230), 25, (255, 0, 0, 0), ba, game.g2),
                      game.t1("Override previous loaded/saved game", (450, 130), 28, (255, 0, 0, 0), ba, game.g2)]
        self.fade, self.load3, self.an, r = [-1, 1], 0, [], ra.randint
        for i in range(60):
            self.an.append(py.shapes.Triangle(x := r(10, 890), y := r(600, 1200), x + r(1, 7), y + r(1, 6), x + r(1, 6),
                                              y - r(1, 7), (255, 255, 255),
                                              batch2))  # generate random triangles-snowflakes for start screen

        class p:  # prevents repeated clicks from holding down!!
            def __init__(self):
                self.p, self.p1 = 0, 1

            def a(self, b=0):
                if self.p: b, self.p1 = self.p1, 0
                return self.p and b

        self.p = p()  # to test a single click use p.a() instead of p.p

    def update(self, dt):
        self.clear(), self.push_handlers(self.keys), py.gl.glClearColor(0, 0.7, 1, 1)
        if g.stats["lives"] < 1 and not self.end and not self.show_scores:
            self.end = 1  # initialise sql variables only once
            self.con = sqlite3.connect("scores.db")
            self.cur = self.con.cursor()  # scoretable/leaderboard initialization
            self.cur.execute("""create table if not exists scores(
             name string not null,round integer not null)""")
            self.cur.execute("select name from scores")
            self.d, self.text = self.cur.fetchall(), ""
            self.text1[1].text = "Not valid, name already taken"
        elif self.save:  # initialise sql and variables for saving-only initialised once
            self.text1[1].text = "Not valid, code already being used"
            self.save, self.save1 = 0, 1
            self.sql()
        elif self.load:  # same as above but for game loading
            self.text1[1].text = "Not valid, no code found"
            self.load, self.load1 = 0, 1
            self.sql()
        elif self.show_scores:
            ba.draw(), self.scores[1].draw()
        elif self.save1:
            if ut.active(*self.xy, self.text1[2]) and self.load2 != "":
                self.text1[2].colour = (255, 255, 0, 255)
                self.text1[2].font_size = 32
                if self.p.a():
                    self.load3 = 1
                    self.text1[2].colour, self.text1[2].font_size = (0, 0, 0, 0), 28
            elif self.load2 != "" and not ut.active(*self.xy, self.text1[2]):
                self.text1[2].colour = (210, 210, 0, 255)
                self.text1[2].font_size = 28
            ba.draw(), self.back(), s.save(self, g, q), self.snow()
        elif self.load1:
            ba.draw(), self.back(), s.load(self, g, q), self.snow()
        elif self.end:
            ba.draw(), s.scores(self, g.stats["round"]), self.back(), self.snow()
        elif self.pause:
            if not s.n: s.rect.draw()
            s.run(self), self.snow()
            if not s.n: self.back(), self.text1[0].draw()
        else:
            if not g.pause: q.run(g, dt)
            g.run(self, q, dt), ba.draw(), queue.batch.draw(), game.b1.draw()
            proteins.batch.draw(), game.b2.draw(), game.b3.draw()
            if g.up.antibody.on: g.up.antibody.circle.draw()
            for j in proteins.towers:
                if type(j).__name__ == "Utilities" and j.water[0] > 0: j.circle.draw()

    def on_draw(self):
        self.p.a()
        # print(py.clock.get_fps())

    def on_mouse_motion(self, x, y, dx, dy):
        self.xy = [x, y]  # mouse x/y position update

    def on_mouse_press(self, x, y, b, m):
        self.xy, self.p.p = [x, y], 1

    def on_mouse_release(self, x, y, b, m):
        self.p.p1, self.p.p = 1, 0

    def on_mouse_drag(self, x, y, dx, dy, b, m):
        self.xy, self.dxy, self.p.p = [x, y], [dx, dy], 1

    def on_key_press(self, k, m):
        if k == key.ESCAPE:
            self.close()  # quick close
        elif self.end or self.save1 or self.load1:  # backspace
            if k == key.BACKSPACE and len(self.text) > 0:
                self.text = self.text[:-1]  # utilises stack-deletes the last placed in element-LIFO
            elif k == key.ENTER and len(self.text) > 0:
                self.enter = 1  # submit code (name->save/load game)
        if k == key.P: g.stats["lives"] = 0  # quick test, also test certain enemies/unlock all towers
        # elif k==key._1: q.active.append(e.en["3"](*q.l[0],queue.batch,game.g2,0))
        # elif k==key._2: q.active.append(e.en["c"](*q.l[0],queue.batch,game.g2,0))
        # elif k==key._3: q.active.append(e.en["v"](*q.l[0],queue.batch,game.g2,0))
        # elif k==key._4: q.active.append(e.en["h"](*q.l[0],queue.batch,game.g2,0))
        # elif k==key._5: q.active.append(e.en["l"](*q.l[0],queue.batch,game.g2,0))
        # elif k==key._9:
        #   a=g.filled-1
        #   for j in list(game.unlock.values())[g.filled-3:]:
        #     for i in range(len(j)):
        #       g.side.append(py.sprite.Sprite((n:=g.grid[(a:=a+1)])[2],n[0]+38,n[1]+38,batch=game.b1,group=game.g3))
        #   g.filled=len(game.pr2)

    def on_key_release(self, k, m):
        if k == key.ENTER: self.enter = 0

    def on_text(self, t):  # user text input for leaderboard/game save/game load
        if self.end or self.load1 or self.save1:
            if len(self.text) < 13 and t != " " and t != "\n" and t != "\r":
                self.text += str(t)

    def sql(self):
        ut.default("load", s.text, s.defaults), ut.default("save", s.text, s.defaults)
        self.text1[0].colour = (210, 210, 0, 255)
        self.con = sqlite3.connect("saves.db")
        self.cur = self.con.cursor()
        self.cur.execute("pragma foreign_keys=on")  # allows functional foreign key use
        self.cur.execute(players), self.cur.execute(towers)
        self.cur.execute("select ID from players")
        self.d, self.text = self.cur.fetchall(), ""

    def back(self):
        if self.fade[0] > -1:
            self.fade = [f[0] + 6, 1] if (f := self.fade)[1] and f[0] < 249 else [f[0] - 6, 0]
            self.text1[1].colour = (255, 0, 0, self.fade[0])
        if self.fade[0] < 0:
            self.fade[1] = True
            self.text1[1].colour = (255, 0, 0, 0)
        if ut.active(*self.xy, self.text1[0]) and not self.end:
            self.text1[0].colour = (255, 255, 0, 255)
            self.text1[0].font_size = 52
            if self.p.a():
                for i in s.images: i.opacity = 0
                for i in s.text1: i.color = (*i.color[:3], 0)
                self.text1[2].colour = (0, 0, 0, 0)
                self.fade, self.text1[1].colour = [-1, 1], (0, 0, 0, 0)
                self.load1, self.text1[0].font_size = 0, 45
                self.save1, self.text1[0].colour = 0, (0, 0, 0, 0)
                s.n, s.info, s.guide, s.credit = 1, [0, 5], 0, 0
                for i in s.text.keys(): ut.default(i, s.text, s.defaults)
        elif not self.end:
            self.text1[0].colour = (210, 210, 0, 255)
            self.text1[0].font_size = 45

    def snow(self):
        for i in self.an:
            i.y, i.y2, i.y3 = i.y - (r := abs(i.x - i.x3)), i.y2 - r, i.y3 - r
            if i.y < 0: i.y, i.y2, i.y3 = i.y + (r := ra.randint(600, 1000)), i.y2 + r, i.y3 + r
            i.opacity = (o := i.opacity) + ra.randint(-5 if o > 50 else 0, 5 if o < 200 else 0)
        batch2.draw()


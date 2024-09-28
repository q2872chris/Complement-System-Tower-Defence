import pyglet as py
import webbrowser
from files import utilities as ut, game as g, proteins as pr

b, s, b1 = py.graphics.Batch(), "Complement System Tower Defence", py.graphics.Batch()


class screen:
    def __init__(self):
        self.rect = py.shapes.BorderedRectangle(0, 0, 900, 600, 6, (0, 180, 255), (0, 150, 0), b, g.g1)
        text = [["title", s, (450, 540), 42, (0, 0, 0, 255), b, g.g2, True],
                ["start", "Start", (450, 350), 80, (210, 210, 0, 255), b, g.g2],
                ["info", "Players Guide", (450, 250), 55, (210, 210, 0, 255), b, g.g2],
                ["exit", "Exit", (450, 160), 55, (210, 210, 0, 255), b, g.g2],
                ["info1", "Science'y info", (210, 40), 45, (210, 210, 0, 255), b, g.g2],
                ["credit", "Credits", (780, 40), 45, (210, 210, 0, 255), b, g.g2],
                ["load", "Load Game", (175, 450), 45, (210, 210, 0, 255), b, g.g2],
                ["save", "Save Game", (730, 450), 45, (210, 210, 0, 255), b, g.g2],
                ["back", "Last Page", (150, 50), 40, (210, 210, 0, 0), b, g.g2],
                ["forward", "Next Page", (750, 50), 40, (210, 210, 0, 0), b, g.g2]]
        d = [24, (0, 0, 0, 0), b1, None, False, 0, True, "left", 860]
        self.images = [py.image.load("images/new1.png"), py.image.load("images/new2.png")]
        for i in range(len(self.images)): self.images[i] = py.sprite.Sprite(self.images[i], 100, 70, batch=b1,
                                                                            group=g.g1)
        for i in self.images: i.opacity, i.scale = 0, 1.4
        self.text1 = [g.t1("Biology info credits to YouTube channel Kurzgesagt and Wikipedia", (450, 430), *d[:3]),
                      g.t1("Game idea credits to Emily Jack", (450, 390), *d[:3]),  # text for screens-info/etc
                      g.t1("Code/everything else credits to me", (450, 350), *d[:3]),
                      g.t1("Complement system video link", (450, 250), 27, (255, 0, 255, 0), b1, None, True, 1),
                      g.t1(
                          "-Tower defence game, drag and drop towers as normal to fight off waves of enemies. Click play to start a new round." +
                          "\n-You can also combine certain towers together to make new ones. New towers will be unlocked throughout so make " +
                          "sure to try combinations. " +
                          "All towers are upgradable/downgradable/and sellable (click on them after they've been placed to view them), some have extra " +
                          "information and special upgrades/abilities.\n-The game can be saved at any point with a code and loaded again later. There " +
                          "is a leaderboard for highest wave reached. \n-Some extra info can be found on the Science'y info page. Try to keep " +
                          "the tower viewing (upgrades/info/etc) rectangle closed during waves due to lag. Enjoy the game",
                          (20, 500), *d),
                      g.t1(
                          "-The complement system is the system of proteins in our bodies that act as part of the immune system. " +
                          "\n-The proteins drift around in a passive state most of the time, until activated by other parts of the immune system " +
                          "(e.g. antibodies) or by pathogens. When this happens they change their shape, meaning they can now interact and fit " +
                          "together with other proteins. \n-The alternative pathway starts with C3, which once activated, splits into C3a and C3b, C3a " +
                          "travels away from the area of pathogens to call for help from other immune cells (e.g. phagocytes). The immune cells then " +
                          "travel back along towards the fight and become more aggressive as they find more alarmed C3a proteins.",
                          (20, 500), *d),
                      g.t1(
                          "-After the C3 splits the C3b can then combine with a B protein, have its shape changed by a D protein, combine with " +
                          "a P protein, and then change its shape again to form C3 Convertase.\n-C3bBb is the alternative pathway version of C3 " +
                          "Convertase.\n-C3 Convertase acts as a recruiting platform to activate " +
                          "more C3's to split into C3b's and C3a's to form more C3 Convertase proteins. \n-These embed themselves in the pathogens, " +
                          "slowing them down and crippling them. \n-In addition C3 Convertase proteins act as hooks in the bacteria so other immune cells " +
                          "can grab (and engulf) them without the bacteria slipping away.", (20, 500), *d),
                      g.t1(
                          "-The Lytic or terminal pathway starts when another C3b protein combines with a C3 Convertase, forming C5 Convertase." +
                          "\n-C5 Convertase can then activate C5 proteins to split them into C5b and C5a, C5b can then combine with C6, C7, C8, " +
                          "and then change itself to form a larger structure, the Membrane Attack Complex. C9 proteins then attach to this protein " +
                          "and force open holes in the bacteria, ripping it apart. \n-Certain pathogens have built up defences against complement " +
                          "however, the vaccinia virus can hijack cells to produce complement control proteins, creating safe zones for the virus, " +
                          "and some bacteria can take molecules out of the blood to become invisible to complement",
                          (20, 500), *d),
                      g.t1("-In the game most proteins can't " +
                           "target 'camo' enemies (they have auras), and the vaccinia enemy stops all towers in its range attacking when it passes. " +
                           "There are also higher health enemies with auras that fade but they don't represent any real pathogen. " +
                           "\n-Complement in real life are tiny, much smaller than pathogens, there would really be 1000's to one pathogen, in this " +
                           "game the roles are reversed to make it work for a tower defence style game. \n-There are two other complement " +
                           "pathways used to create C3 Convertase, the classical and lectin pathways.", (20, 500), *d),
                      g.t1(
                          "-The classical pathway begins with the C1 Complex (containing the C1q, C1r, and C1s proteins) \n-Once C1q is " +
                          "activated it can activate C1r, which then activates C1s.\n-C1s then cleaves (splits) C4 into C4b and C4a, and " +
                          "C2 into C2b and C2a.\n-C4b and C2b then combine to make C4b2b (C3 Convertase)", (20, 500),
                          *d),
                      g.t1(
                          "-The lectin pathway starts with MBL, multimers of MBL combine with MASP-1,2,and 3.\n-Once MASP-1 and " +
                          "MASP-2 are activated they start cleaving C4 and C2 like in the classical pathway. \n-After C3 Convertase " +
                          "is created it follows on in the same way as the end of the alternative pathway and the terminal/lytic pathway.\n" +
                          "-The proteins (eg B) can also be referred to as factors.", (20, 500), *d),
                      g.t1("-More information on the complement system can be found by playing the game (there is an "
                           "info button on each tower which gives some more basic info on the proteins), in addition there is a toggleable info button " +
                           "which allows you to see which other towers (proteins) a protein can combine with before it's placed instead of its cost. The " +
                           "credits page contains a link to the Kurzgesagt video explaining the same concepts on the complement system.\n" +
                           "-There are some discrepancies between sources but I've tried to make everything clear in the individual protein " +
                           "tower info pages, along with any unrealistic game elements.", (20, 500), *d),
                      g.t1("Kurzgesagt's representation of the various protein types (not the combined ones)",
                           (20, 500), 24, (255, 255, 0, 0), b1, g.g2, True, 0, True, "left", 860),
                      g.t1("Kurzgesagt's representation of the protein pathway's (combination processes)",
                           (20, 500), 24, (255, 255, 0, 0), b1, g.g2, True, 0, True, "left", 860)]
        self.text, self.guide = {i[0]: g.t1(*i[1:]) for i in text}, 0
        self.defaults, self.n, self.credit, self.info = {i[0]: g.t1(*i[1:]) for i in text}, 1, 0, [0, 5]
        for i in self.defaults.values(): i.batch = None

    def run(self, win):
        if self.credit:
            if ut.active(*win.xy, self.text1[3]):
                self.text1[3].font_size = 30
                if win.p.a(): webbrowser.open("https://www.youtube.com/watch?v=BSypUV6QUNw")  # hyperlink
            else:
                self.text1[3].font_size = 27
        if self.info[0]:
            if ut.active(*win.xy, self.text["back"]) and self.info[1] > 5:
                self.text["back"].font_size, self.text["back"].colour = 45, (255, 255, 0, 255)
                if win.p.a():
                    self.text1[self.info[1]].colour = (*self.text1[self.info[1]].colour[:3], 0)
                    self.info[1] -= 1
                    self.text1[self.info[1]].colour = (*self.text1[self.info[1]].colour[:3], 255)
                    self.text["forward"].colour = (*self.text["forward"].colour[:3], 255)
                    if self.info[1] == 5:
                        self.text["back"].colour = (*self.text["back"].colour[:3], 0)
                    elif self.info[1] == len(self.text1) - 2:
                        self.images[0].opacity, self.images[1].opacity = 255, 0
                    elif self.info[1] < len(self.text1) - 2:
                        self.images[0].opacity = 0
            elif self.info[1] > 5:
                self.text["back"].font_size, self.text["back"].colour = 40, (210, 210, 0, 255)
            if ut.active(*win.xy, self.text["forward"]) and self.info[1] < len(self.text1) - 1:
                self.text["forward"].font_size, self.text["forward"].colour = 45, (255, 255, 0, 255)
                if win.p.a():  # way of changing text opacity without changing (or needing to know original) colour!
                    self.text1[self.info[1]].colour = (*self.text1[self.info[1]].colour[:3], 0)
                    self.info[1] += 1
                    self.text1[self.info[1]].colour = (*self.text1[self.info[1]].colour[:3], 255)
                    self.text["back"].colour = (*self.text["back"].colour[:3], 255)
                    if self.info[1] == len(self.text1) - 1:
                        self.text["forward"].colour = (*self.text["forward"].colour[:3], 0)
                        self.images[0].opacity, self.images[1].opacity = 0, 255
                    elif self.info[1] == len(self.text1) - 2:
                        self.images[0].opacity = 255  # checks-chained pages
            elif self.info[1] < len(self.text1) - 1:
                self.text["forward"].font_size, self.text["forward"].colour = 40, (210, 210, 0, 255)
        if not self.n:
            b1.draw(), self.text["title"].draw()
            if self.info[0]: self.text["back"].draw(), self.text["forward"].draw()
        else:
            b.draw()
            for i in list(self.text.keys())[1:8]:
                if ut.active(*win.xy, self.text[i]):
                    if i == "exit" and win.p.a():
                        win.close()
                    elif i == "start" and win.p.a():
                        ut.default(i, self.text, self.defaults)
                        self.text[i].text, win.pause = "Resume", 0
                        break  # win.p.a() mustn't be the 1st condition
                    elif i == "load" and win.p.a():
                        win.load = 1
                    elif i == "save" and win.p.a():
                        win.save = 1
                    elif i == "credit" and win.p.a():
                        self.n, self.credit = 0, 1
                        for j in range(4): self.text1[j].colour = (*self.text1[j].colour[:3], 255)
                    elif i == "info" and win.p.a():
                        self.n, self.guide = 0, 1
                        self.text1[4].colour = (*self.text1[4].colour[:3], 255)
                    elif i == "info1" and win.p.a():
                        self.n, self.info[0] = 0, 1
                        self.text1[5].colour = (*self.text1[5].colour[:3], 255)
                        self.text["forward"].colour = (*self.text["forward"].colour[:3], 255)
                    if i == "start":
                        self.text[i].font_size = 90
                    elif i == "info1" or i == "credit" or i == "save" or i == "load":
                        self.text[i].font_size = 52
                    else:
                        self.text[i].font_size = 60
                    self.text[i].colour = (255, 255, 0, 255)
                else:
                    ut.default(i, self.text, self.defaults)

    @staticmethod  # built in decorator
    def scores(win, r):  # sql
        def check(c, t, f=0):
            while True:
                f += 1  # check one at a time-conserve memory
                if c.fetchone()[0] == t: return f

        g.t1(win.text, (450, 300), 50, y := (255, 255, 0, 255), ba := py.graphics.Batch())
        g.t1("Game over", (450, 460), 35, (100, 30, 0, 225), ba, None, True, 1)
        g.t1("Input name for leaderboard, Enter to submit", (450, 400), 30, (0, 0, 0, 255), ba), ba.draw()
        if name(win.text, win.d, win) and win.enter:  # unique names only
            win.cur.execute("insert into scores(name,round) values(?,?)", [win.text, r])
            win.cur.execute("select * from scores order by round desc limit 10")
            win.show_scores, win.enter, b2 = 1, 0, py.graphics.Batch()  # specific selection
            a, t1 = win.cur.fetchall(), "Complement system tower defence leaderboard"
            win.cur.execute("select * from scores where name='%s'" % win.text)  # overloaded modulus operator
            a1, p3, u = win.cur.fetchall(), [30, y, b2, None, True, 1, False, "left"], " (you)"
            p, p1, p2 = lambda x: " (you)" if x[0] == win.text else "", " reached wave: %s", "(%s) "
            d = [g.t1(p2 % (i + 1) + a[i][0] + p1 % a[i][1] + p(a[i]), (200, 470 - 40 * i), *p3) for i in range(len(a))]
            if a1[0] not in a:  # include current player at bottom if not in top 10
                win.cur.execute("select name from scores order by round desc")
                d += [g.t1(p2 % check(win.cur, win.text) + a1[0][0] + p1 % a1[0][1] + u, (200, 470 - 40 * len(a)), *p3)]
            d += [g.t1(t1, (450, 550), 32, (0, 0, 0, 255), b2, None, True)]
            win.scores = [d, b2]  # text
            win.con.commit(), win.con.close()

    @staticmethod  # static method
    def save(win, ga, q):  # more sql
        t, t1 = "Input code to save game, use to load game", "next time, Enter to submit"
        g.t1(win.text, (450, 300), 50, (255, 255, 0, 255), ba := py.graphics.Batch())
        g.t1(t, (450, 430), 30, (0, 0, 0, 255), ba), g.t1(t1, (450, 380), 30, (0, 0, 0, 255), ba), ba.draw()
        if (name(win.text, win.d, win) and win.enter) or win.load3:
            if win.load3:  # update-use foreign key to automatically delete related towers
                win.text = win.load2  # don't keep duplicates after overriding, can reuse code
                win.cur.execute(
                    "delete from players where ID='%s'" % win.text)  # need the modulus operator surrounded with quotes to be read as a string properly
            r1 = ga.stats["round"] if not q.pause else ga.stats["round"] - 1
            l = [ga.stats["gold"], ga.stats["lives"], q.wait[1], ga.filled, q.last]
            win.cur.execute("""insert into players(ID,round,gold,lives,speed,fill,place)
           values(?,?,?,?,?,?,?)""", [win.text, r1, *l])
            for i in pr.towers:  # get stats for each tower to upload
                d, co, w, r, co1, sell = i.difference()
                l1 = [str(d), str(co), w, r, str(co1), sell]
                if type(i).__name__ != "temp C3a":
                    win.cur.execute("""insert into towers(ID,x,y,type,count,d,co,w,r,co1,sell)
             values(?,?,?,?,?,?,?,?,?,?,?)""", [win.text, i.x, i.y, i.name, i.count, *l1])
            win.con.commit(), win.con.close()
            win.load2, win.load3, win.text1[2].colour = win.text, 0, (0, 0, 0, 0)
            win.save1, win.text1[0].colour, win.text1[1].colour, win.fade = 0, (0, 0, 0, 0), (0, 0, 0, 0), [-1, 1]

    def load(self, win, ga, q):  # more sql
        g.t1(win.text, (450, 300), 50, (255, 255, 0, 255), ba := py.graphics.Batch())
        g.t1("Input code to load game, Enter to submit", (450, 400), 30, (0, 0, 0, 255), ba), ba.draw()
        if name(win.text, win.d, win) and win.enter: win.fade[0] = 0
        if not name(win.text, win.d, win) and win.enter:
            win.cur.execute("""select gold,lives,round,speed,fill,place from players
           where ID='%s'""" % win.text), pr.towers.clear(), q.active.clear()
            ga.stats["gold"], ga.stats["lives"] = (a := win.cur.fetchall()[0])[:2]
            ga.stats["round"], q.wait[1], ga.filled, q.read = a[2:]  # reset stats
            pr.batch = py.graphics.Batch()
            ga.fill(), ga.queue.clear()
            win.cur.execute("""select x,y,type,count,co,d,w,r,co1,sell from players as p inner join
           towers as t on p.ID=t.ID and p.ID=?""", (win.text,))
            for i in win.cur.fetchall():  # using inner join and on as opposed to using where
                co1 = [int(i) for i in i[8][1:-1].split(",")]
                co = [float(i) for i in i[4][1:-1].split(",")]
                d = [int(i) for i in i[5][1:-1].split(",")]
                pr.towers.append(
                    pr.proteins[i[2]](i[0], i[1], i[3], d, co, i[6], i[7], co1, i[9]))  # re-instantiate towers
            win.load1, win.load2, self.text["start"].text = 0, win.text, "Resume"
            q.pause, q.r_pause, win.pause, ga.auto = 0, 0, 0, 0
            win.fade, win.text1[1].colour, win.text1[0].colour = [-1, 1], (0, 0, 0, 0), (0, 0, 0, 0)
            for i in ga.stats.keys(): ga.update(i, 0)
            win.con.commit(), win.con.close()


def name(c, l, win):  # unique names check
    if c in [i[0] for i in l]:
        if win.enter: win.fade[0] = 0
        return False
    return True

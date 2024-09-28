import pyglet as py
import maths
from pyglet import shapes
from files import game as g, enemies as e, proteins as pr

batch, op = py.graphics.Batch(), open("text/waves")  # initialise string to read enemy types from
string = op.read()
op.close()


class queue:
    def __init__(self):  # track vertices
        self.l = (l := [[60, -20], [60, 150], [100, 100], [300, 100], [60, 500], [450, 500], [450, 350], [250, 350],
                        [250, 280], [340, 280], [440, 240], [520, 340], [600, 340], [680, 240], [500, 180], [500, -20]])
        self.circles = [shapes.Circle(*l[i], 15, None, (0, 255, 0), batch, g.g1) for i in range(len(l) - 1)]
        self.lines = [shapes.Line(*l[i], *l[i + 1], 30, (0, 255, 0), batch, g.g1) for i in range(len(l) - 1)]
        self.vecs = [[*l[i], l[i + 1][0] - l[i][0], l[i + 1][1] - l[i][1], *l[i + 1]] for i in range(len(l) - 1)]
        self.d = [math.sqrt(self.vecs[i][2] ** 2 + self.vecs[i][3] ** 2) for i in
                  range(len(l) - 1)]  # distances/vectors
        self.wait, self.read, self.pause, self.r_pause, self.active, self.last = [1, 30], 0, 0, 0, [], 0

    def run(self, w, dt):
        if self.pause and self.r_pause and self.wait[0] == 0: self.new_wave(w)
        if self.pause: self.running(w, dt)
        self.wait[0] = self.wait[0] + 1 if 0 < self.wait[0] < self.wait[1] else 0  # control read speed

    def running(self, w, dt, a=50):
        for i in self.active:
            for k in pr.towers:
                if type(i).__name__ == "vaccinia" and (i.x - k.x) ** 2 + (i.y - k.y) ** 2 < i.range ** 2:
                    k.wait[0] = 1  # if enemy is vaccinia type-stop all towers in range being able to attack
                if type(k).__name__ == "MBL" and (i.x - k.x) ** 2 + (i.y - k.y) ** 2 < k.range ** 2:
                    a = 30  # slower speed if in MBL tower range
                    break
            vx, vy = dt * a * self.vecs[i.i][2] * i.v / self.d[i.i], dt * a * self.vecs[i.i][3] * i.v / self.d[
                i.i]  # normalise vectors
            if min(i.x, i.x + vx) <= self.l[i.i + 1][0] <= max(i.x, i.x + vx):
                if min(i.y, i.y + vy) <= self.l[i.i + 1][1] <= max(i.y, i.y + vy):  # check for next vector
                    i.x, i.y, i.i, vx, vy = self.l[i.i + 1][0], self.l[i.i + 1][1], i.i + 1, 0, 0
            if i.i == len(self.l) - 1:  # delete if reach end
                w.update("lives", -i.damage), self.active.pop(self.active.index(i))
            elif i.health < 1:  # create new enemy if available (nested enemy relationship)
                if str(i.base) != "0": self.active.append(e.en[str(i.base)](i.x, i.y, batch, g.g2, i.i,
                                                                            i.health))  # health is carried across to the enemy it turns into when it dies, this means if the damage dealt was greater than the health it will automatically reduce the health and deal the correct amount of damage through all layers
                w.update("gold", i.gold), self.active.pop(self.active.index(i))
            else:
                i.x, i.y, i.vx, i.vy = i.x + vx, i.y + vy, vx, vy  # enemy velocity components
                i.sprite.update(i.x, i.y), i.run()

    def new_wave(self, w):
        try:
            self.read, b, self.wait[0] = self.read + 1, batch, 1
            if string[self.read] == "p":  # new round-pause
                if w.auto:
                    w.update((f := "round"), 1), w.queue.append("Wave %s" % w.stats[f])  # auto feature
                else:
                    self.r_pause, self.last = 0, self.read
            elif string[self.read] == "s":
                self.wait[1] -= 2  # increase read speed
            elif (a := string[self.read]) != "0" and a != "\n" and a != " ":
                self.active.append(e.en[a](*self.l[0], b, g.g2, 0))  # create new enemy instance
        except ValueError:
            pass
        except IndexError:
            pass

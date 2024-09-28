from pyglet import shapes as s


class pro1:
    def __init__(self, x, y, vx: float, vy: float, b, p):
        self.rect = s.Rectangle(x - 2, y - 2, 4, 4, (0, 0, 0), b)
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.p, self.count = p, 1
        self.life, self.damage = p.data1, p.data2

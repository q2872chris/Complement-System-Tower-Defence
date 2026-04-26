import pyglet as py
from itertools import product
from drawables import BRect, Rect, Line, Sprite, Label
from globals import game_attrs

g = py.graphics.OrderedGroup


class Scroller:
    def __init__(self, protein_sprites: list[Sprite], protein_counts: list[Label]):
        batch = game_attrs.batch
        self.mouse = game_attrs.mouse
        y2 = 395 - 75 * (len(protein_sprites) + len(protein_sprites) % 2) // 2
        coords = sorted(product((700, 775), range(395, y2, -75)), key=lambda x: -x[1])
        self.tiles = [BRect(x, y, 75, 75, 5, (70, 0, 0), (200, 0, 200), batch, g(2))
                      for x, y in coords]
        self.red_rects = [Rect(x + 2, y + 2, 71, 71, (255, 0, 0), batch, g(4), 100)
                          for x, y in coords]
        for rect in self.red_rects:
            rect.hide()
        self.side_panel = BRect(700, 0, 200, 470, 5, (70, 0, 0), (200, 0, 200), batch, g(1))
        self.lines = [
            Line(700, 470, 900, 470, 4, (200, 0, 200), batch, g(4)),
            Line(700, 0, 700, 600, 4, (200, 0, 200), batch, g(4)),
            Line(850, 0, 850, 470, 3, (200, 0, 200), batch, g(4))
        ]
        self.bar = BRect(854, 360, 38, 103, 6, (100, 255, 100), (0, 0, 0), batch, g(2))
        self.active = False
        self.scroll = False
        self.y = 0
        self.scale_y = (-y2 - 75) / 352
        self.scroll_speed = 13
        for sprite, label, (x, y) in zip(protein_sprites, protein_counts, coords):
            sprite.update(x + 38, y + 38)
            label.update(x + 62, y + 15)
        self.rects = [*self.tiles, *self.red_rects, *protein_sprites, *protein_counts]

    def update(self):
        if not self.mouse.scroll:
            self.scroll = False
        elif not self.scroll and self.mouse.scroll and self.side_panel.collide_point(*self.mouse.pos()):
            self.scroll = True
        if not self.mouse.click:
            self.active = False
            self.mouse.release_focus("scroll")
        elif not self.active and self.mouse.get_click() and self.bar.collide_point(*self.mouse.pos()):
            self.active = True
            self.y = self.mouse.y
            self.mouse.set_focus("scroll")
        if self.active:
            move = max(min(self.y - self.mouse.y, self.bar.y - 7), self.bar.y - 360)
            self.scroll_rects(move * self.scale_y)
            self.bar.y -= move
            self.y = self.mouse.y
        elif self.scroll:
            move = max(min(-self.mouse.dy * self.scroll_speed, self.bar.y - 7), self.bar.y - 360)
            self.scroll_rects(move * self.scale_y)
            self.bar.y -= move

    def scroll_rects(self, y: int):
        for rect in self.rects:
            rect.y += y




import pyglet as py
from drawables import Button, Sprite, Label
from screens import BaseScreen, goto_screen
from globals import game_attrs
from itertools import product
from utilities import extend

g = py.graphics.OrderedGroup


class EnemiesScreen(BaseScreen):
    batch = py.graphics.Batch()

    def __init__(self):
        super().__init__()
        self.sprites_and_labels = []
        self.xy = list(product(range(470, 80, -70), range(80, 870, 140)))
        buttons = {
            name: Button("o", x, y, 40, 40, (0, 0, 0, 0), (0, 0, 0, 0),
                         self.batch, g(1), quick_action=goto_screen(name))
            for (name, e), (y, x) in zip(game_attrs.enemy_classes.items(), self.xy)
        }
        self.__dict__.update(**buttons)
        self.back_button = Button("Back", 450, 50, 40, 45, (210, 210, 0, 255),
                                  (255, 255, 0, 255), self.batch, g(1),
                                  quick_action=goto_screen("PortfoliosHomeScreen"))

    @extend
    def build_sprites(self):
        self.sprites_and_labels = [
            [Sprite(e.img, x, y, self.batch, g(1), scale=1.6),
             Label(e.__name__, x, y + 26, 11, (255, 255, 0, 255),
                   self.batch, g(2), italic=True)]
            for e, (y, x) in zip(game_attrs.enemy_classes.values(), self.xy)
        ]



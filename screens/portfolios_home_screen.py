import pyglet as py
from drawables import Button
from screens import BaseScreen, goto_screen

g = py.graphics.OrderedGroup


class PortfoliosHomeScreen(BaseScreen):
    batch = py.graphics.Batch()

    def __init__(self):
        super().__init__()
        self.towers_button = Button("Towers", 250, 310, 60, 65, (210, 210, 0, 255),
            (255, 255, 0, 255), self.batch, g(1), quick_action=goto_screen("TowersScreen"))
        self.enemies_button = Button("Enemies", 650, 310, 60, 65, (210, 210, 0, 255),
            (255, 255, 0, 255), self.batch, g(1), quick_action=goto_screen("EnemiesScreen"))
        self.back_button = Button("Back", 450, 50, 40, 45, (210, 210, 0, 255),
            (255, 255, 0, 255), self.batch, g(1), quick_action=goto_screen("TitleScreen"))





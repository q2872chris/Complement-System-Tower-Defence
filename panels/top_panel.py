import pyglet as py
from drawables import BRect, Label, Button
from globals import game_attrs

g = py.graphics.OrderedGroup


class TopPanel:
    def __init__(self):
        batch = game_attrs.batch
        self.panel = BRect(700, 470, 199, 130, 5, (0, 0, 0), (200, 0, 200), batch, g(5))
        self.tower_name = Label("", 800, 560, 25, (255, 255, 0, 255), batch, g(6))
        self.tower_cost = Label("", 800, 530, 18, (0, 255, 255, 255), batch, g(6))
        self.tower_base = Label("", 800, 505, 18, (100, 255, 0, 255), batch, g(6))
        self.info_button = Button("info", 665, 505, 18, 20, (255, 255, 255, 200),
                                  (255, 255, 155, 255), batch, g(3), False, True,
                                  (0, 255, 0, 200), (0, 255, 0, 255))

    def update_text(self, tower):
        self.tower_name.text = tower.__name__
        self.tower_cost.text = f"£{tower.cost}"
        self.tower_base.text = tower.show_base if self.info_button.on else ""

    def update(self, mouse):
        self.info_button.hover(mouse, "top_panel")





import pyglet as py
from abc import ABC
from protein_towers.panels import BaseTowerPanel
from drawables import Button, ButtonUp
from globals import game_attrs
from game_elements.floating_tower import FloatingTowerMovement

g = py.graphics.OrderedGroup


class SellablePanel(BaseTowerPanel, ABC):
    """Implements selling and moving."""
    def __init__(self, tower, previous_panel):
        self.sell_button = Button("Sell", 100, 60, 18, 20, (200, 200, 0, 200), (250, 250, 0, 255),
                                  self.batch, g(8), quick_action=self.sell_tower)
        self.move_button = ButtonUp("Move", 100, 90, 18, 20,
                                  (0, 200, 0, 200), (0, 250, 0, 255),
                                  self.batch, g(8), quick_action=self.move)
        super().__init__(tower, previous_panel)

    def sell_tower(self):
        self.game_attrs.gold += self.tower.sell_cost
        self.placed_towers.remove(self.tower)
        self.tower.sprite.delete()
        self.tower.label.delete()
        if len(self.tower.components) > 1:
            self.split(self.tower.components)
        else:
            self.split(self.tower.components, static=True)
        self.deactivate()

    def split(self, ids: list, static=False):
        self.tower.split(ids, static)

    def move(self):
        game_attrs.announcement.activate(f"{self.tower.name} test-message", once=True)
        self.tower.floating_tower = FloatingTowerMovement(self.tower)
        self.tower.sprite.opacity = 150
        self.mouse.set_focus("move_tower", override=True)
        self.deactivate()






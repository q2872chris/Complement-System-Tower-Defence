import pyglet as py
from abc import ABC
from protein_towers.panels import SellablePanel
from drawables import Label, Button, BRect

g = py.graphics.OrderedGroup


class UpgradablePanel(SellablePanel, ABC):
    def __init__(self, tower, previous_panel):
        Y = 470
        num_keys = len(tower.upgrade_keys)
        self.rects = [BRect(10 + x, Y - 50 - y, 18, 12, 3, (255, 0, 0), (255, 255, 255),
                            self.batch, g(8))
                      for y in range(0, 50 * num_keys, 50) for x in range(0, 120, 30)]
        self.upgrade_texts = [
            Label("", 10, Y - 20 - y, 14, (255, 255, 255, 255), self.batch, g(8), anchor_x="left")
            for y in range(0, 50 * num_keys, 50)
        ]
        self.upgrade_cost_texts = [
            Label("", 125, Y - 44 - y, 13, (255, 255, 255, 255), self.batch, g(8), anchor_x="left")
            for y in range(0, 50 * num_keys, 50)
        ]
        self.upgrade_buttons = [
            Button("(+)", 180, Y - 20 - y, 15, 18, (200, 200, 0, 200), (255, 255, 0, 255),
                   self.batch, g(8), quick_action=self.upgrade(ind))
            for ind, y in enumerate(range(0, 50 * num_keys, 50))
        ]
        self.set_upgrade_data(tower)
        super().__init__(tower, previous_panel)

    def set_upgrade_data(self, tower):
        for ind, key in enumerate(tower.upgrade_keys):
            title = key.capitalize().replace('_', ' ')
            self.upgrade_texts[ind].text = f"{title}: {getattr(tower, key)}"
            self.upgrade_cost_texts[ind].text = f"£{tower.upgrade_costs[ind]}"
            for i in range(4):
                colour = (255, 0, 0) if i >= tower.upgrade_nums[ind] else (0, 255, 0)
                self.rects[ind * 4 + i].color = colour

    def upgrade(self, ind: int):
        def inner():
            cost = self.tower.upgrade_costs[ind]
            if cost <= self.game_attrs.gold and self.tower.upgrade_nums[ind] < 4:
                self.game_attrs.gold -= cost
                self.tower.upgrade(ind)
            self.set_upgrade_data(self.tower)
            self.tower_cost.text = f"Sell price: £{self.tower.sell_cost}"
        return inner



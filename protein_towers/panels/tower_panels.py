import pyglet as py
from abc import ABC
from drawables import Label, Button, ButtonUp, BRect
from protein_towers.panels import UpgradablePanel, SellablePanel
from globals import game_attrs

g = py.graphics.OrderedGroup


def BlankPanel(_self, _tower, _previous_panel):
    return None


class MBLPanel(UpgradablePanel, ABC):
    def __init__(self, tower, previous_panel):
        self.C9_label = Label(f"C9s: {tower.C9s}", 10, 140, 15, (255, 255, 255, 255),
                              self.batch, g(8), False, True, "left", "bottom")
        self.blue_rects = [
            BRect(10 + x, 125 - y, 17, 12, 3, (0, 0, 255), (255, 255, 255), self.batch, g(8))
            for y in (0, 20) for x in range(0, 170, 23)
        ]
        for i in range(tower.C9s):
            self.blue_rects[i].color = (0, 255, 0)
        super().__init__(tower, previous_panel)


class StaticGhostTowerPanel(SellablePanel, ABC):
    def __init__(self, tower, previous_panel):
        self.active_label = Label("", 10, 140, 15, (255, 255, 255, 255),
                                  self.batch, g(8), False, True, "left", "bottom")
        super().__init__(tower, previous_panel)

    def update(self):
        self.active_label.text = f"Time remaining: {self.tower.max_time - self.tower.time}"
        super().update()


class CleavablePanel(UpgradablePanel, ABC):
    def __init__(self, tower, previous_panel):
        self.cleave_button = Button("Self-Cleave", 100, 120, 18, 20,
                                    (0, 200, 200, 200), (0, 250, 250, 255),
                                    self.batch, g(8), quick_action=self.cleave)
        super().__init__(tower, previous_panel)

    def cleave(self):
        self.placed_towers.remove(self.tower)
        return_gold = int(self.tower.sell_cost - self.tower.cost * self.tower.sell_modifier)
        self.game_attrs.gold += return_gold
        self.split(self.tower.self_cleave)
        game_attrs.announcement.activate(f"{self.tower.name} spontaneously cleaved", once=True)
        self.deactivate()


class ActivatablePanel(UpgradablePanel, ABC):
    def __init__(self, tower, previous_panel):
        self.active_text = "Active: %s"
        self.active_mod = {True: "Yes", False: "No"}
        self.active_label = Label(self.active_text % self.active_mod[tower.active],
                                  10, 140, 15, (255, 255, 255, 255),
                                  self.batch, g(8), False, True, "left", "bottom")
        self.activate_cost = Label(f"Activate cost: £{tower.activate_cost}",
                                   10, 160, 15, (255, 255, 255, 255),
                                   self.batch, g(8), False, True, "left", "bottom")
        super().__init__(tower, previous_panel)


class SelfActivatablePanel(ActivatablePanel, ABC):
    def __init__(self, tower, previous_panel):
        self.activate_button = Button("Auto-Activate", 100, 120, 18, 20,
                                      (0, 200, 200, 200), (0, 250, 250, 255),
                                    self.batch, g(8), quick_action=self.auto_activate)
        super().__init__(tower, previous_panel)

    def auto_activate(self):
        if not self.tower.active:
            game_attrs.announcement.activate(f"{self.tower.name} auto-activated", once=True)
            self.tower.active = True
            self.active_label.text = self.active_text % self.active_mod[True]
            game_attrs.gold -= self.tower.activate_cost
            self.tower.sprite.opacity = 255


class PowerUpTowerPanel(UpgradablePanel, ABC):
    def __init__(self, tower, previous_panel):
        self.cooldown_label = Label("", 10, 132, 15, (255, 255, 255, 255),
                                    self.batch, g(8), False, True, "left", "bottom")
        if not hasattr(self, "deactivate_flag"):
            self.deactivate_flag = False
        if not hasattr(self, "cost"):
            self.cost = 0
        super().__init__(tower, previous_panel)

    def powerup(self):
        if self.tower.powerup_cooldown == 0:
            game_attrs.gold -= self.cost
            self.tower.powerup()
            self.tower.powerup_cooldown = 1
            if self.deactivate_flag:
                self.deactivate()

    def update(self):
        time = self.tower.powerup_maxcooldown - self.tower.powerup_cooldown
        self.cooldown_label.text = f"Cooldown left: {time}"
        super().update()


class OverclockTowerPanel(PowerUpTowerPanel, ABC):
    def __init__(self, tower, previous_panel):
        self.cost = 40
        self.powerup_button = Button(f"Overclock (£{self.cost})", 100, 120, 18, 19,
                                     (0, 200, 200, 200), (0, 250, 250, 255),
                                     self.batch, g(8), quick_action=self.powerup)
        super().__init__(tower, previous_panel)


class C3aBackupTowerPanel(PowerUpTowerPanel, ABC):
    def __init__(self, tower, previous_panel):
        self.cost = 30
        self.powerup_button = Button(f"Get support (£{self.cost})", 100, 120, 18, 19,
                                     (0, 200, 200, 200), (0, 250, 250, 255),
                                     self.batch, g(8), quick_action=self.powerup)
        super().__init__(tower, previous_panel)


class AntibodyTowerPanel(PowerUpTowerPanel, ABC):
    def __init__(self, tower, previous_panel):
        self.cost = 35
        self.powerup_button = ButtonUp(f"Antibody (£{self.cost})", 100, 120, 18, 19,
                                       (0, 200, 200, 200), (0, 250, 250, 255),
                                       self.batch, g(8), quick_action=self.powerup)
        self.deactivate_flag = True
        super().__init__(tower, previous_panel)


class ManualSpikeTowerPanel(PowerUpTowerPanel, ABC):
    def __init__(self, tower, previous_panel):
        self.cost = 25
        self.powerup_button = ButtonUp(f"Spike pile (£{self.cost})", 100, 120, 18, 19,
                                       (0, 200, 200, 200), (0, 250, 250, 255),
                                       self.batch, g(8), quick_action=self.powerup)
        self.deactivate_flag = True
        super().__init__(tower, previous_panel)
        self.tower_game_info.y -= 45


class RadialShotTowerPanel(UpgradablePanel, ABC):
    def __init__(self, tower, previous_panel):
        super().__init__(tower, previous_panel)
        self.buttons.remove(self.target_button)
        self.target_button.delete()
        self.tower_name.y -= 10
        self.tower_cost.y -= 10
        self.pop_count.y += 10






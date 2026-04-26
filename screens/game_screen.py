import pyglet as py
from panels import ProteinsPanel
from enemies import EnemyController
from drawables import RectBorder
from globals import game_attrs
from screens import BaseScreen

g = py.graphics.OrderedGroup


class GameScreen(BaseScreen):
    batch = game_attrs.batch

    def __init__(self):
        super().__init__()
        self.mouse = game_attrs.mouse
        self.announcement = game_attrs.announcement
        self.placed_towers = game_attrs.placed_towers
        self.main_panel = game_attrs.main_panel
        self.top_panel = game_attrs.top_panel
        self.proteins_shop_panel = ProteinsPanel()
        self.enemy_controller = EnemyController()
        self.border = RectBorder(0, 0, 900, 600, 6, (200, 0, 200), self.batch, g(5))
        self.tower_panel = None
        self.enemy_controller.end_round_func = self.main_panel.end_play

    def update(self, dt: float):
        """Update order is important due to mouse focus priority."""
        if self.mouse.has_focus("", "main_panel"):
            self.main_panel.update()
        if not game_attrs.paused:
            if self.mouse.has_focus("", "top_panel"):
                self.top_panel.update(self.mouse)
            self.announcement.update()
            if self.tower_panel is None or self.tower_panel.side == "left":
                self.proteins_shop_panel.update()
            if self.tower_panel is None or self.mouse.pos() not in self.tower_panel:
                self.check_tower_clicks()
            if self.tower_panel is not None:
                if self.tower_panel.active:
                    self.tower_panel.update()
                else:
                    self.tower_panel = None
            for tower in self.placed_towers:
                tower.update(dt)
            self.enemy_controller.update(dt)
            self.update_projectiles(dt)
            # Stop dragging onto things while holding down
            if self.mouse.get_click():
                self.mouse.set_focus("stop")
            elif not self.mouse.click:
                self.mouse.release_focus("stop")

    @staticmethod
    def update_projectiles(dt: float):
        for projectile in game_attrs.projectiles:
            projectile.run(dt)

    def check_tower_clicks(self):
        for tower in self.placed_towers:
            if self.mouse.pos() in tower.sprite and self.mouse.get_click():
                self.mouse.set_focus("tower_click")
                self.tower_panel = tower.activate_panel(self.tower_panel)
                break
        if not self.mouse.click:
            self.mouse.release_focus("tower_click")
        if self.tower_panel is not None and self.mouse.get_click("", "floating_tower") \
                and self.mouse.pos() not in self.tower_panel:
            self.tower_panel.deactivate()
            self.tower_panel = None





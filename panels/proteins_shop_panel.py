from panels import Scroller
from game_elements import FloatingTowerShop
from globals import game_attrs


class ProteinsPanel:
    """Stores the top panel."""
    def __init__(self):
        self.mouse = game_attrs.mouse
        self.game_attrs = game_attrs
        self.placed_towers = game_attrs.placed_towers
        self.proteins = game_attrs.proteins
        self.shop_towers = game_attrs.shop_towers
        self.top_panel = game_attrs.top_panel
        self.track = game_attrs.track
        protein_sprites = [protein.sprite for protein in self.shop_towers.values()]
        protein_counts = [protein.count_label for protein in self.shop_towers.values()]
        self.scroller = Scroller(protein_sprites, protein_counts)
        self.active: (FloatingTowerShop | None) = None
        self.last_viewed_tower = next(iter(self.shop_towers.values()))
        self.clicked = False
        self.drag = False
        self.click_check = True
        self.last_pos = (0, 0)

    def update(self):
        self.update_grid()
        self.scroller.update()
        if self.active is None and not self.scroller.active:
            self.tower_click()
            if self.last_viewed_tower is not None:
                self.top_panel.update_text(self.last_viewed_tower)
        if self.active is None and not self.mouse.click:
            self.mouse.release_focus("floating_tower")
        if self.active is not None:
            self.active.run()
            if (self.mouse.click and self.clicked) or (not self.mouse.click and self.drag):
                self.active = None
                self.clicked = False
                self.drag = False

    def tower_click(self):
        for rect, tower in zip(self.scroller.tiles, self.shop_towers.values()):
            if tower.unlocked and self.mouse.pos() in rect:
                self.last_viewed_tower = tower
                self.top_panel.update_text(tower)
                if self.mouse.get_click() and not self.clicked:
                    self.mouse.set_focus("floating_tower")
                    self.last_pos = self.mouse.pos()
                    self.clicked = True
                if not self.mouse.click and self.clicked:
                    if tower.cost <= self.game_attrs.gold and tower.number > 0:
                        self.active = FloatingTowerShop(tower, clicked=True)
                        tower.sprite.hide()
                        tower.count_label.hide()
        if self.mouse.click and self.clicked and self.last_pos != self.mouse.pos():
            self.clicked = False
            self.drag = True
            if self.last_viewed_tower.cost <= self.game_attrs.gold and \
                    self.last_viewed_tower.number > 0 and self.active is None:
                self.active = FloatingTowerShop(self.last_viewed_tower, drag=True)
                self.last_viewed_tower.sprite.hide()
                self.last_viewed_tower.count_label.hide()

    def update_grid(self):
        for tower, rect in zip(self.shop_towers.values(), self.scroller.red_rects):
            if tower.cost <= self.game_attrs.gold and tower.number > 0:
                rect.hide()
            elif tower.unlocked:
                rect.show()

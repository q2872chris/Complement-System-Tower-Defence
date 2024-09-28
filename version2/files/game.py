from files.panels import tower_panel
from files.utilities import text
from files.data import window_data as win
# 'floating' placement?

class game:
    def __init__(self, towers):
        self.towers = towers
        self.lives = 30
        self.lives_text = text(-1, f"lives: {self.lives}", x=win.game_width * 0.99, italic=True,
            y=win.window_height * 0.93, font_size=20, color=(255, 255, 255, 150), anchor_x="right")
        self.panel = tower_panel()
        self.panel_on = False

    def update(self, x, y, click):  # placement!
        for i in self.towers:
            if (x, y) in i and click:
                self.panel_on = True
                self.panel.set(x, i)
                break
        else:
            if click and (x, y) not in self.panel:
                self.panel_on = False
                self.panel.reset()
        if self.panel_on and (x, y) in self.panel:
            if self.panel.update(x, y, click):
                self.panel_on = False
                self.panel.reset()



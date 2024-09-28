from files import components, statics
from files.data import game_data, window_data as win
from files.utilities import text
from files.other import format_number

class panel:
    def __init__(self, grid, speed, texts):             # write better statics container
        self.static_sprites = statics.generate_statics()     # 0th element is side_panel
        self.grid = grid
        self.speed = speed
        self.tower_range = components.tower_range()
        self.bar = components.scroller()
        self.name_text = texts.name
        self.cost_text = texts.cost
        self.combine_text = texts.combine
        first_protein = grid[0].protein
        self.name_text.update_text(first_protein.__name__, True)      # edit text creation?
        self.cost_text.update_text(f"£{first_protein.cost}", True)
        self.move = False
        self.pickup = False
        self.tower = None
        self.money = 1_000
        self.money_text = text(x=win.game_width * 0.99, italic=True, y=win.window_height * 0.97,
            font_size=20, color=(255, 255, 255, 150), anchor_x="right")
        self.buy(1)

    def info(self):
        pass

    def buy(self, flag: int):   # make sure combination cost > tower cost
        if flag == 2:
            self.money -= self.tower.return_combination('cost')
        elif flag == 0:
            self.money -= self.tower.cost
        self.money_text.update_text(f"Amino acids: {format_number(self.money)}")
        for i in self.grid:
            i.update_money(self.money)

    def tower_pickup(self, x, y, click):
        for i in self.grid:
            if (x, y) in i:
                tower = i.protein
                self.name_text.update_text(tower.__name__, True)
                self.cost_text.update_text(f"£{tower.cost}", True)
                self.combine_text.update_text(tower.show_base, True)
                if click and not i.locked:
                    self.pickup = True
                    self.tower = tower
                    self.tower.update_pos(x, y)
                    self.tower_range.update(x, y, tower.range, 100)
                    break

    def tower_move(self, x, y):
        self.tower.update_pos(x, y)     # more functions!
        colour = self.tower.place_check(x, y)
        self.tower_range.update(x, y, colour=colour)
        if colour == 2:     # need to create proper text classes so they can default back
            self.name_text.update_text(self.tower.return_combination())
            self.cost_text.update_text(f"£{self.tower.return_combination('cost')}")
            self.combine_text.update_text("")
        else:
            self.name_text.update_text()
            self.cost_text.update_text()
            self.combine_text.update_text()

    def tower_place(self, x, y):
        place_check = self.tower.place_check(x, y)
        self.pickup = False
        self.tower_range.update(opacity=0)
        self.tower.update_pos()
        self.tower.initialise(x, y)
        self.buy(place_check)

    def update(self, x, y, dy, click):
        if not game_data.tower_panel_allow_scroll:
            return
        self.check_scroll_bar(x, y, dy, click)
        if not self.pickup and not self.move and (x, y) in self.static_sprites[0]:
            self.tower_pickup(x, y, click)
        elif self.pickup and click:
            self.tower_move(x, y)
        elif self.pickup and not click:
            self.tower_place(x, y)

    def check_scroll_bar(self, x, y, dy, click):
        if click and not self.pickup and (x, y) in self.bar:
            self.move = True
        elif not click:
            self.move = False
        if self.move:
            self.move_panel(dy)

    def scroll(self, x, y, dy):
        if not game_data.tower_panel_allow_scroll:
            return
        if (x, y) in self.static_sprites[0]:
            self.move_panel(dy * 10)

    def move_panel(self, dy):  # needs scaling for expandability
        if self.bar.update(dy):
            for i in self.grid:
                i.update(dy * self.speed)


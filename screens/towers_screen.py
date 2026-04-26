import pyglet as py
from drawables import Button, Sprite, Label
from globals import game_attrs
from screens import BaseScreen, goto_screen
from utilities import extend
from itertools import product

g = py.graphics.OrderedGroup
xy = list(product(range(445, 80, -80), range(80, 870, 140)))
pathways = ("Alternative", "Terminal/Lytic", "Classical", "Lectin")
keys = ("Alternative", "Lytic", "Classical", "Lectin")
orders = [
    ("C3", "C3b", "C3a", "B", "D", "P", "Bb", "Ba",
     "C3bB", "C3bBb", "C3bBbP", "C3bBbC3b", "C3bBbPC3b"),
    ("C3bBbC3b", "C3bBbPC3b", "C4b2b3b", "C5", "C5b", "C5a", "C6", "C7", "C8", "C9",
     "C5b-6", "C5b-7", "C5b-8", "C5b-9", *[f"C5b-9({n})" for n in range(2, 17)]),
    ("C3", "C3b", "C3a", "C1q", "C1r", "C1s", "C1rC1s", "C1r2C1s2", "C1 Complex",
     "C2", "C2b", "C2a", "C4", "C4b", "C4a", "C4bC2", "C4b2b", "C4b2b3b"),
    ("C3", "C3b", "C3a", "MBL", "MASP-1", "MASP-2",
     "C2", "C2b", "C2a", "C4", "C4b", "C4a", "C4bC2", "C4b2b", "C4b2b3b")
]


class TowersScreen(BaseScreen):
    batch = py.graphics.Batch()

    def __init__(self):
        super().__init__()
        self.tower_buttons = [{}, {}, {}, {}]
        self.sprites_and_labels = [[], [], [], []]
        self.pathway_title = Label("", 30, 510, 25, (255, 255, 255, 255), self.batch,
                                   g(1), italic=True, bold=True, anchor_x="left")
        self.protein_lists = [
            sorted([(key, value) for key, value in game_attrs.proteins.items()
                    if keys[i] in value.pathway], key=lambda v: orders[i].index(v[0]))
            for i in range(4)
        ]
        for ind, pathway_list in enumerate(self.protein_lists):
            for (name, p), (y, x) in zip(pathway_list, xy):
                self.tower_buttons[ind][f"{name}_{pathways[ind]}"] = Button(
                    "o", x, y, 45, 45, (0, 0, 0, 0), (0, 0, 0, 0), self.batch, g(1),
                    quick_action=goto_screen(name)
                )
        for dictionary in self.tower_buttons:
            self.__dict__.update(**dictionary)
        self.back_button = Button("Back", 450, 50, 40, 45, (210, 210, 0, 255),
                                  (255, 255, 0, 255), self.batch, g(1),
                                  quick_action=self.portfolios_home_screen)
        self.next_button = Button("Next", 800, 50, 35, 40, (210, 210, 0, 255),
                                  (255, 255, 0, 255), self.batch, g(1),
                                  quick_action=self.forward, disable_on_click=False)
        self.previous_button = Button("Previous", 120, 50, 35, 40, (210, 210, 0, 255),
                                      (255, 255, 0, 255), self.batch, g(1),
                                      quick_action=self.previous, disable_on_click=False)
        self.page = 1
        self.loaded_pages = [False] * 4

    @extend
    def build_sprites(self):
        self.loaded_pages[self.page - 1] = True
        pathway_list = self.protein_lists[self.page - 1]
        for (name, p), (y, x) in zip(pathway_list, xy):
            self.sprites_and_labels[self.page - 1] += [
                Sprite(p.img, x, y, self.batch, g(1)),
                Label(name, x, y + 26, 11, (255, 255, 0, 255),
                      self.batch, g(2), italic=True)
            ]
        self.hide()

    def portfolios_home_screen(self):
        game_attrs.current_screen = "PortfoliosHomeScreen"
        self.page = 1
        self.hide()

    def hide(self):
        for i in {*range(len(self.tower_buttons))} - {self.page - 1}:
            for button in self.tower_buttons[i].values():
                button.hide()
            for obj in self.sprites_and_labels[i]:
                obj.hide()
        for button in self.tower_buttons[self.page - 1].values():
            button.show()
        for obj in self.sprites_and_labels[self.page - 1]:
            obj.show()
        self.pathway_title.text = f"{pathways[self.page - 1]} pathway:"
        if self.page == 1:
            self.previous_button.hide()
            self.next_button.show()
        elif self.page == len(self.tower_buttons):
            self.next_button.hide()
            self.previous_button.show()
        else:
            self.previous_button.show()
            self.next_button.show()

    def forward(self):
        if self.page < len(self.tower_buttons):
            self.page += 1
        if not self.loaded_pages[self.page - 1]:
            self.build_sprites()
        self.hide()

    def previous(self):
        if self.page > 1:
            self.page -= 1
        self.hide()




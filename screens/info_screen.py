import pyglet as py
from drawables import Label, Button, Sprite
from globals import game_attrs
from screens import BaseScreen
from utilities import extend

g = py.graphics.OrderedGroup

with open("text/info_text.txt") as reader:
    text = reader.read().split("\n\n")


class InfoScreen(BaseScreen):
    batch = py.graphics.Batch()

    def __init__(self):
        super().__init__()
        self.text: (Label | None) = None
        self.back_button = Button("Back", 450, 40, 40, 45, (210, 210, 0, 255),
                                  (255, 255, 0, 255), self.batch, g(1),
                                  quick_action=self.title_screen)
        self.next_button = Button("Next", 800, 40, 35, 40, (210, 210, 0, 255),
                                  (255, 255, 0, 255), self.batch, g(1),
                                  quick_action=self.forward, disable_on_click=False)
        self.previous_button = Button("Previous", 120, 40, 35, 40, (210, 210, 0, 255),
                                      (255, 255, 0, 255), self.batch, g(1),
                                      quick_action=self.previous, disable_on_click=False)
        self.sprites: dict[int, Sprite] = {}
        self.pages = [{"text": i, "color": (255, 255, 0, 255) if ind > 6 else (0, 0, 0, 255)}
                      for ind, i in enumerate(text)]
        self.page = 1

    @extend
    def build_sprites(self):
        self.text = Label(text[0], 10, 510, 23, (0, 0, 0, 255), self.batch, g(2), anchor_x="left",
                          anchor_y="top", multiline=True, width=880)
        images = {8: py.image.load("images/proteins.png"),
                  9: py.image.load("images/full_pathways.png"),
                  10: py.image.load("images/pathway.png"),
                  11: py.image.load("images/C3bB.png")}
        self.sprites = {i: Sprite(im, 100, 70, self.batch, g(1), scale=1.4)
                        for i, im in images.items()}
        self.hide_sprites()
        self.previous_button.hide()

    def title_screen(self):
        self.page = 1
        self.text.set_kwargs(**self.pages[0])
        self.previous_button.hide()
        self.next_button.show()
        self.hide_sprites()
        game_attrs.current_screen = "TitleScreen"

    def forward(self):
        if self.page < len(self.pages):
            self.page += 1
            self.text.set_kwargs(**self.pages[self.page - 1])
            self.previous_button.show()
            self.hide_sprites()
        if self.page == len(self.pages):
            self.next_button.hide()
        if self.page in self.sprites:
            self.sprites[self.page].show()

    def previous(self):
        if self.page > 1:
            self.page -= 1
            self.text.set_kwargs(**self.pages[self.page - 1])
            self.next_button.show()
            self.hide_sprites()
        if self.page == 1:
            self.previous_button.hide()
        if self.page in self.sprites:
            self.sprites[self.page].show()

    def hide_sprites(self):
        for sprite in self.sprites.values():
            sprite.hide()





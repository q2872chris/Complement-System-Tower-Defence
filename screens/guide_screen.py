import pyglet as py
from drawables import Label, Button
from screens import BaseScreen, goto_screen
from utilities import extend

g = py.graphics.OrderedGroup

with open("text/guide_text.txt") as reader:
    text = reader.read()


class GuideScreen(BaseScreen):
    batch = py.graphics.Batch()

    def __init__(self):
        super().__init__()
        self.back_button = Button("Back", 450, 40, 40, 45, (210, 210, 0, 255),
                                  (255, 255, 0, 255), self.batch, g(1),
                                  quick_action=goto_screen("TitleScreen"))

    @extend
    def build_sprites(self):
        Label(text, 10, 510, 23, (0, 0, 0, 255), self.batch, g(1), anchor_x="left",
              anchor_y="top", multiline=True, width=880)




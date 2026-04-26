import pyglet as py
import webbrowser
from drawables import Label, Button
from screens import BaseScreen, goto_screen
from utilities import extend
# from pyglet.text.document import FormattedDocument

g = py.graphics.OrderedGroup

with open("text/credits_text.txt") as reader:
    text = reader.read()


class CreditsScreen(BaseScreen):
    batch = py.graphics.Batch()

    def __init__(self):
        super().__init__()
        self.back_button = Button("Back", 450, 60, 40, 45, (210, 210, 0, 255),
                                  (255, 255, 0, 255), self.batch, g(1),
                                  quick_action=goto_screen("TitleScreen"))
        self.link_button = Button("Complement system video link", 450, 280, 40, 41,
                                  (200, 0, 200, 200), (200, 0, 200, 240), self.batch, g(1),
                                  italic=True, quick_action=self.link)

    @extend
    def build_sprites(self):
        Label(text, 450, 480, 23, (0, 0, 0, 255), self.batch, g(1),
              anchor_y="top", multiline=True, width=880, align="center")


    @staticmethod
    def link():
        webbrowser.open("https://www.youtube.com/watch?v=BSypUV6QUNw")



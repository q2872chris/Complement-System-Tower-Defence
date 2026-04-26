import pyglet as py
from drawables import Button
from globals import game_attrs
from screens import BaseScreen, goto_screen

g = py.graphics.OrderedGroup


class CheckStartScreen(BaseScreen):
    batch = py.graphics.Batch()

    def __init__(self):
        super().__init__()
        self.main_button = Button("Are you sure?", 450, 350, 60, 65, (210, 210, 0, 255),
                                  (255, 255, 0, 255), self.batch, g(1),
                                  quick_action=self.start_new_game)
        self.back_button = Button("Back", 450, 200, 50, 55, (210, 210, 0, 255),
                                  (255, 255, 0, 255), self.batch, g(1),
                                  quick_action=goto_screen("TitleScreen"))
        self.on_start_new_game = lambda x=0: None  # To be initialised in GameController

    def start_new_game(self):
        game_attrs.paused = False
        game_attrs.set_defaults()
        self.on_start_new_game()
        game_attrs.current_screen = "GameScreen"





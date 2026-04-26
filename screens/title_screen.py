import pyglet as py
from drawables import Button
from globals import game_attrs
from screens import BaseScreen, goto_screen

g = py.graphics.OrderedGroup


class TitleScreen(BaseScreen):
    batch = py.graphics.Batch()

    def __init__(self):
        super().__init__()
        self.start_button = Button("Start New Game", 450, 350, 50, 55, (210, 210, 0, 255),
                                   (255, 255, 0, 255), self.batch, g(1),
                                   quick_action=self.start_new_game)
        self.resume_button = Button("Resume Game", 450, 260, 50, 55, (210, 210, 0, 255),
                                    (255, 255, 0, 255), self.batch, g(1),
                                    quick_action=self.resume_game)
        self.resume_button.hide()
        self.load_button = Button("Load Game", 190, 450, 50, 55, (210, 210, 0, 255),
                                  (255, 255, 0, 255), self.batch, g(1),
                                  quick_action=goto_screen("LoadScreen"))
        self.save_button = Button("Save Game", 710, 450, 50, 55, (210, 210, 0, 255),
                                  (255, 255, 0, 255), self.batch, g(1),
                                  quick_action=goto_screen("SaveScreen"))
        self.guide_button = Button("Players Guide", 220, 170, 50, 55, (210, 210, 0, 255),
                                   (255, 255, 0, 255), self.batch, g(1),
                                   quick_action=goto_screen("GuideScreen"))
        self.portfolios_button = Button("Portfolios", 700, 170, 50, 55, (210, 210, 0, 255),
                                   (255, 255, 0, 255), self.batch, g(1),
                                   quick_action=goto_screen("PortfoliosHomeScreen"))
        self.exit_button = Button("Exit", 450, 80, 50, 55, (210, 210, 0, 255),
                                  (255, 255, 0, 255), self.batch, g(1),
                                  quick_action=self.exit)
        self.science_info_button = Button("Science", 160, 70, 50, 55, (210, 210, 0, 255),
                                          (255, 255, 0, 255), self.batch, g(1),
                                          quick_action=goto_screen("InfoScreen"))
        self.credits_button = Button("Credits", 745, 70, 50, 55, (210, 210, 0, 255),
                                     (255, 255, 0, 255), self.batch, g(1),
                                     quick_action=goto_screen("CreditsScreen"))
        self.on_start_new_game = lambda x=0: None   # To be initialised in GameController

    def start_new_game(self):
        if self.resume_button.visible:
            game_attrs.current_screen = "CheckStartScreen"
        else:
            game_attrs.paused = False
            game_attrs.set_defaults()
            self.on_start_new_game()
            game_attrs.current_screen = "GameScreen"

    @staticmethod
    def resume_game():
        game_attrs.paused = False
        game_attrs.current_screen = "GameScreen"

    @staticmethod
    def exit():
        game_attrs.quit = True



import pyglet as py
from pyglet.window import key
from drawables import BRect, Rect, Label, Button
from globals import game_attrs

g = py.graphics.OrderedGroup


class MainPanel:
    def __init__(self):
        batch = game_attrs.batch
        self.panel = BRect(0, 0, 700, 600, 5, (0, 179, 255), (200, 0, 200), batch, g(0))
        self.gold_label = Label("", 690, 580, 20, (255, 255, 255, 255), batch, g(1),
                                anchor_x="right")
        self.lives_label = Label("", 690, 555, 20, (255, 255, 255, 255), batch, g(1),
                                anchor_x="right")
        self.waves_label = Label("", 690, 530, 20, (255, 255, 255, 255), batch, g(1),
                                 anchor_x="right")
        self.pause_button = Button("pause", 652, 480, 18, 20, (255, 255, 255, 200),
                                   (255, 255, 155, 255), batch, g(3), False, True,
                                   quick_action=self.pause)
        self.play_button = Button("play", 660, 455, 18, 20, (255, 255, 255, 200),
                                  (255, 255, 155, 255), batch, g(3), False, True,
                                  (0, 255, 0, 200), (0, 255, 0, 255),
                                  on_action=self.play, lock_on=True)
        self.auto_button = Button("auto", 660, 430, 18, 20, (255, 255, 255, 200),
                                  (255, 255, 155, 255), batch, g(3), False, True,
                                  (0, 255, 0, 200), (0, 255, 0, 255),
                                  quick_action=self.auto)
        self.resume_button = Button("Resume", 450, 310, 60, 65, (200, 200, 0, 200),
                                    (200, 200, 0, 250), batch, g(11),
                                    quick_action=self.resume)
        self.title_screen_button = Button("Title Screen", 450, 190, 60, 65,
                                          (200, 200, 0, 200), (200, 200, 0, 250),
                                          batch, g(11), quick_action=self.title_screen)
        self.pause_text = Label("Paused", 450, 500, 90, (50, 50, 50, 150), batch, g(11))
        self.pause_rect = Rect(0, 0, 900, 600, (120, 120, 120), batch, g(10), 100)
        self.pause_items = [self.pause_rect, self.resume_button, self.pause_text,
                            self.title_screen_button]
        for item in self.pause_items:
            item.hide()
        self.mouse = game_attrs.mouse
        self.buttons = [self.auto_button, self.play_button, self.pause_button]

    def switch_buttons_on_load(self):
        if self.play_button.on:
            self.play_button.switch_colours()
        if game_attrs.auto:
            self.auto_button.switch_colours()

    @staticmethod
    def play():
        if not game_attrs.round_active:
            game_attrs.wave += 1
            game_attrs.round_active = True

    def end_play(self):
        if not game_attrs.auto:
            self.play_button.switch_colours()

    @staticmethod
    def auto():
        game_attrs.auto = not game_attrs.auto

    def pause(self):
        game_attrs.paused = True
        for item in self.pause_items:
            item.show()

    def resume(self):
        game_attrs.paused = False
        for item in self.pause_items:
            item.hide()

    def title_screen(self):
        for item in self.pause_items:
            item.hide()
        game_attrs.current_screen = "TitleScreen"

    def update(self):
        self.gold_label.text = f"Gold: {game_attrs.gold}"
        self.lives_label.text = f"Lives: {game_attrs.lives}"
        self.waves_label.text = f"Wave: {game_attrs.wave}"
        if game_attrs.paused:
            self.resume_button.hover(self.mouse, "main_panel")
        if game_attrs.paused:  # Deliberately repeated
            self.title_screen_button.hover(self.mouse, "main_panel")
        else:
            for button in self.buttons:
                button.hover(self.mouse, "main_panel")

    def on_key_press(self, symbol: int, _modifiers: int):
        if game_attrs.current_screen == "GameScreen":
            if symbol == key.G:
                game_attrs.gold += 1000
            # H = Health with L = Lead
            elif symbol == key.H:
                game_attrs.lives += 100
            # R = Round start with P = Purple
            elif symbol == key.R and not game_attrs.round_active:
                self.play_button.switch_colours()
            elif symbol == key.A:
                self.auto_button.switch_colours()






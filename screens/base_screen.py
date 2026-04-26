import pyglet as py
from drawables import Label, Button, Star, RectBorder
from globals import game_attrs
from utilities import extend
from random import randint

g = py.graphics.OrderedGroup


class Snowflake(Star):
    def __init__(self, batch: py.graphics.Batch):
        super().__init__(x=randint(10, 890), y=randint(0, 800), outer_radius=randint(5, 6),
                         inner_radius=randint(1, 2), num_spikes=randint(3, 7),
                         colour=(255, 255, 255), batch=batch, group=g(2),
                         opacity=randint(90, 170))
        self.rotation_speed = 1
        self.speed = randint(100, 150)

    def animate(self, dt: float):
        self.y -= self.speed * dt
        self.rotation += self.rotation_speed
        if self.y < 0:
            self.y += randint(600, 800)


def init_decorator(init):
    def new_init(self, *args, **kwargs):
        init(self, *args, **kwargs)
        self.__post_init__()
    return new_init


class BaseScreen:
    batch = py.graphics.Batch()
    border = RectBorder(0, 0, 900, 600, 6, (0, 150, 0), batch, g(5))
    title = Label("Complement System Tower Defence 4", 450, 560, 39,
                  (0, 0, 0, 255), batch, g(1), bold=True)
    snowflakes = list(map(lambda b: Snowflake(b), [batch] * randint(50, 70)))

    def __init__(self):
        self.mouse = game_attrs.mouse
        self.buttons: list[Button] = []
        self.loaded = False

    def __post_init__(self):
        self.buttons = [i for i in self.__dict__.values() if isinstance(i, Button)]

    def __init_subclass__(cls):
        cls.__init__ = init_decorator(cls.__init__)

    def update(self, dt: float):
        for button in self.buttons:
            if button.visible:
                button.hover(self.mouse, type(self).__name__)
        for snowflake in self.snowflakes:
            snowflake.animate(dt)

    def build_sprites(self):
        """Deferred rendering."""
        self.loaded = True


class Typer(BaseScreen):
    """Used for Save and Load screens."""
    def __init__(self):
        super().__init__()   # noqa
        self.back_button = Button("Back", 450, 40, 40, 45, (210, 210, 0, 255),
                                  (255, 255, 0, 255), self.batch, g(1),
                                  quick_action=self.title_screen)
        self.writing = Label("", 450, 300, 25, (0, 0, 0, 255), self.batch, g(1))
        self.text = ""
        self.max_length = 13
        self.stop_funcs = []

    @extend
    def build_sprites(self):
        Label("Write your code here:", 450, 400, 30,
              (0, 0, 100, 255), self.batch, g(1), True, True)

    def active_check(self) -> bool:
        return game_attrs.current_screen == type(self).__name__

    @extend
    def update(self, dt: float):
        self.writing.text = self.text

    def on_text(self, char: str):
        if self.active_check() and len(self.text) < self.max_length and \
                char != " " and char != "\r":
            self.text += char

    def on_key_press(self, symbol: int, _modifiers: int):
        if self.active_check():
            if symbol == py.window.key.BACKSPACE:
                self.text = self.text[:-1]
            if symbol == py.window.key.ENTER:
                self.title_screen(enter=True)

    def title_screen(self, enter=False):
        game_attrs.current_screen = "TitleScreen"
        if enter:
            for func in self.stop_funcs:
                func()
        self.text = ""
        self.writing.text = ""






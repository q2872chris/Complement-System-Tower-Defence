import pyglet as py
from drawables import Label, Button, Sprite
from screens import BaseScreen, goto_screen
from globals import game_attrs
from typing import Type
from enemies.enemies import EnemyBase
from utilities import extend

g = py.graphics.OrderedGroup


class EnemyTemplateScreen(BaseScreen):
    batch = py.graphics.Batch()

    def __init__(self, enemy: Type[EnemyBase]):
        super().__init__()
        self.enemy = enemy
        self.sprites: list[Sprite] = []
        self.back_button = Button("Back", 450, 50, 40, 45, (210, 210, 0, 255),
             (255, 255, 0, 255), self.batch, g(1), quick_action=goto_screen("EnemiesScreen"))

    @extend
    def build_sprites(self):
        E = self.enemy
        # Name:
        Label("Enemy name:", 20, 510, 20, (255, 255, 255, 255),
              self.batch, g(2), anchor_x="left", italic=True, bold=True)
        Label(E.__name__, 180, 508, 20, (255, 255, 255, 255),
              self.batch, g(2), anchor_x="left", italic=True)
        # Main sprite:
        Label(f"Enemy sprite:", 20, 472, 20, (255, 255, 255, 255),
              self.batch, g(2), anchor_x="left", italic=True, bold=True)
        self.sprites.append(Sprite(E.img, 195, 470, self.batch, g(1)))
        # Info text:
        Label("Enemy info:", 20, 435, 18, (255, 255, 255, 255),
              self.batch, g(1), anchor_x="left", italic=True, bold=True)
        Label(E.info, 20, 415, 20, (255, 255, 255, 255), self.batch,
              g(2), anchor_x="left", anchor_y="top", multiline=True, width=350, italic=True)
        # Enemy attributes:
        Label(f"Enemy attributes:", 600, 510, 18, (255, 255, 255, 255),
              self.batch, g(2), anchor_x="left", italic=True, bold=True)
        attrs_keys = ("speed", "max_health", "full_health", "damage", "full_damage",
                      "value", "full_value", "slow_immune")
        attrs_text = ("Speed", "Layer health", "Full health", "Layer damage", "Full damage",
                      "Layer value", "Full value", "Slow immunity")
        funcs = [lambda a: a] * 7 + [lambda a: "Yes" if a else "No"]
        for (key, text, func, y) in zip(attrs_keys, attrs_text, funcs, range(0, 200, 27)):
            Label(f"{text}: {func(getattr(E, key))}", 600, 482 - y, 16, (255, 255, 255, 255),
                  self.batch, g(2), anchor_x="left", italic=True)
        # Upper:
        Y1 = 35
        Label("Ascended Enemies:", 600, 290 - Y1, 18, (255, 255, 255, 255),
              self.batch, g(1), anchor_x="left", italic=True, bold=True)
        if E.upper:
            for key, x in zip(E.upper, range(0, len(E.upper) * 75, 75)):
                self.sprites.append(Sprite(game_attrs.enemy_classes[key].img,
                                           640 + x, 240 - Y1, self.batch, g(1)))
                Label(game_attrs.enemy_classes[key].__name__, 640 + x, 262 - Y1, 10,
                      (255, 255, 0, 255), self.batch, g(2))
        else:
            Label("None", 810, 289 - Y1, 15, (255, 255, 255, 255), self.batch, g(1),
                  anchor_x="left", italic=True)
        # Bases:
        Label("Enemy spawns:", 600, 200 - Y1, 18, (255, 255, 255, 255),
              self.batch, g(1), anchor_x="left", italic=True, bold=True)
        base_strs = {a: E.bases.count(i) for i in E.bases if
                     (a := game_attrs.enemy_classes.get(i, False))}
        if base_strs.items():
            for (e, n), x in zip(base_strs.items(), range(0, len(base_strs) * 75, 75)):
                self.sprites.append(Sprite(e.img, 640 + x, 150 - Y1, self.batch, g(1)))
                Label(e.__name__, 640 + x, 172 - Y1, 10, (255, 255, 0, 255), self.batch, g(2))
                Label(f"x{n}", 662 + x, 152 - Y1, 12, (255, 255, 0, 255), self.batch, g(2),
                      anchor_x="left")
        else:
            Label("None", 772, 199 - Y1, 15, (255, 255, 255, 255), self.batch, g(1),
                  anchor_x="left", italic=True)
        # Variations:
        Label("Variations:", 20, 280, 18, (255, 255, 255, 255),
              self.batch, g(1), anchor_x="left", italic=True, bold=True)
        Label("Camo:", 30, 250, 16, (255, 255, 255, 255), self.batch, g(1),
              anchor_x="left", italic=True)
        self.sprites.append(Sprite(E.img, 110, 250, self.batch, g(1), opacity=150))
        Label("Regen:", 30, 225, 16, (255, 255, 255, 255), self.batch, g(1),
              anchor_x="left", italic=True)
        self.sprites.append(Sprite(E.img, 115, 225, self.batch, g(1)))
        Label("Camo and regen:", 30, 200, 16, (255, 255, 255, 255), self.batch, g(1),
              anchor_x="left", italic=True)
        self.sprites.append(Sprite(E.img, 210, 200, self.batch, g(1), opacity=150))





import pyglet as py
from drawables import Label, Button, Sprite, Triangle, Circle
from globals import game_attrs
from screens import BaseScreen, goto_screen
from typing import Type
from protein_towers.protein_full_bases import BasicTower
from protein_towers import tower_names
from utilities import extend

g = py.graphics.OrderedGroup


class TowerTemplateScreen(BaseScreen):
    batch = py.graphics.Batch()

    def __init__(self, protein_tower: Type[BasicTower]):
        super().__init__()
        self.protein_tower = protein_tower
        self.sprites = []
        self.bases: list[Sprite | Label] = []
        self.arrows: list[Triangle] = []
        self.combinations: list[Sprite | Label] = []
        self.tower_info_label: (Label | None) = None
        self.tower_info: (Label | None) = None
        self.back_button = Button("Back", 450, 50, 40, 45, (210, 210, 0, 255),
            (255, 255, 0, 255), self.batch, g(1), quick_action=goto_screen("TowersScreen"))

    @extend
    def build_sprites(self):
        P = self.protein_tower
        # Name:
        Label("Protein name:", 10, 510, 20, (255, 255, 255, 255),
              self.batch, g(2), anchor_x="left", italic=True, bold=True)
        Label(P.__name__, 175, 508, 20, (255, 255, 255, 255),
              self.batch, g(2), anchor_x="left", italic=True)
        # Main sprite:
        Label(f"Protein sprite:", 10, 475, 20, (255, 255, 255, 255),
              self.batch, g(2), anchor_x="left", italic=True, bold=True)
        self.sprites.append(Sprite(P.img, 200, 470, self.batch, g(1)))
        # Bases:
        Label("Possible combinations:", 380, 520, 18, (255, 255, 255, 255),
              self.batch, g(2), anchor_x="left", italic=True, bold=True)
        self.bases = [
            [Sprite(game_attrs.proteins[p].img, 420, 475 - y, self.batch, g(1)),
             Label(p, 420, 500 - y, 10, (255, 255, 0, 255), self.batch, g(2))]
            for p, y in zip(P.base, range(0, len(P.base) * 65, 65))
        ]
        # Combinations:
        self.combinations = [
            [Sprite(game_attrs.proteins[p].img, 520, 475 - y, self.batch, g(1)),
             Label(p, 520, 500 - y, 10, (255, 255, 0, 255), self.batch, g(2))]
            for p, y in zip(P.combination, range(0, len(P.base) * 65, 65)) if p != "None"
        ]
        self.arrows = [
            Triangle(465, 485 - y, 465, 465 - y, 483, 475 - y, (255, 255, 255),
                     self.batch, g(1)) for y in range(0, len(P.base) * 65, 65)
        ]
        # Cleaves:
        for cleaves, y in zip(P.cleave, range(0, len(P.base) * 65, 65)):
            for p, x in zip(cleaves, range(0, len(cleaves) * 50, 65)):
                Label(p, 620 + x, 500 - y, 10, (255, 255, 0, 255), self.batch, g(2))
                self.sprites.append(
                    Sprite(game_attrs.proteins[p].img, 620 + x, 475 - y, self.batch, g(1))
                )
        if P.cleave:
            for ind, y in enumerate(range(0, len(P.base) * 65, 65)):
                if len(P.cleave) > ind:
                    Label("&", 570, 475 - y, 25, (255, 255, 255, 255), self.batch, g(2))
        # Components:
        Label("Protein components:", 30, 150, 18, (255, 255, 255, 255),
              self.batch, g(2), anchor_x="left", italic=True, bold=True)
        components = {i: P.components.count(i) for i in P.components}
        for (p, n), x in zip(components.items(), range(0, len(components) * 65, 65)):
            Label(f"x{n}", 82 + x, 102, 12, (255, 255, 0, 255), self.batch, g(2), anchor_x="left")
            Label(p, 60 + x, 125, 10, (255, 255, 0, 255), self.batch, g(2))
            self.sprites.append(
                Sprite(game_attrs.proteins[p].img, 60 + x, 100, self.batch, g(1))
            )
        # Protein info:
        Label("Protein info:", 10, 440, 18, (255, 255, 255, 255), self.batch, g(1),
              anchor_x="left", italic=True, bold=True)
        Label(P.info, 10, 420, 16, (255, 255, 255, 255), self.batch, g(2),
              anchor_x="left", anchor_y="top", multiline=True, width=370, italic=True)
        # Tower type:
        print(P.__mro__)
        tower_type = next(f"{n[:-5]} {n[-5:]}" for i in P.__mro__
                          if (n := i.__name__) in tower_names)
        Label(f"Tower type: {tower_type}", 600, 275, 15, (255, 255, 255, 255),
              self.batch, g(1), anchor_x="left", italic=True, bold=True)
        # Tower attributes:
        Label("Tower initial attributes:", 600, 250, 15, (255, 255, 255, 255),
              self.batch, g(1), anchor_x="left", italic=True, bold=True)
        for i, y in zip(P.upgrade_keys, range(0, 25 * len(P.upgrade_keys), 25)):
            Label(f"{i.capitalize().replace('_', ' ')}: {getattr(P, i)}", 600, 225 - y,
                  14, (255, 255, 255, 255), self.batch, g(1), anchor_x="left", italic=True)
        # Tower powerups:
        Y1 = 0
        Label(f"Tower powerups:", 600, 125 - Y1, 14, (255, 255, 255, 255),
              self.batch, g(1), anchor_x="left", italic=True)
        powerup_text = ", ".join(P.power_ups).capitalize() if P.power_ups else "None"
        Label(powerup_text, 620, 100 - Y1, 14, (255, 255, 255, 255),
              self.batch, g(1), anchor_x="left", italic=True)
        # Tower abilities:
        Label(f"Tower abilities:", 600, 75 - Y1, 14, (255, 255, 255, 255),
              self.batch, g(1), anchor_x="left", italic=True)
        abilities_text = ", ".join(P.abilities).capitalize() if P.abilities else "None"
        Label(abilities_text, 620, 50 - Y1, 14, (255, 255, 255, 255),
              self.batch, g(1), anchor_x="left", italic=True)
        # Tower info:
        self.tower_info_label = Label(f"Tower info:", 400, 250, 15, (255, 255, 255, 255),
            self.batch, g(1), anchor_x="left", italic=True, bold=True)
        self.tower_info = Label(P.game_info, 400, 235, 13, (255, 255, 255, 255), self.batch,
            g(2), anchor_x="left", anchor_y="top", multiline=True, width=180, italic=True)

    def delete(self, obj):
        if obj is None:
            return
        if hasattr(obj, "delete"):
            obj.delete()
        elif isinstance(obj, list):
            for item in obj:
                self.delete(item)


class C9(TowerTemplateScreen):
    batch = py.graphics.Batch()

    @extend
    def build_sprites(self):
        P = self.protein_tower
        self.delete(self.bases)
        self.delete(self.combinations)
        self.delete(self.arrows)
        self.bases = [
            [Sprite(game_attrs.proteins[p].img, 420, 475 - y, self.batch, g(1)),
             Label(p, 420, 500 - y, 10, (255, 255, 0, 255), self.batch, g(2))]
            for p, y in zip(P.base[:3] + [P.base[-1]], (0, 65, 130, 250))
        ]
        self.combinations = [
            [Sprite(game_attrs.proteins[p].img, 520, 475 - y, self.batch, g(1)),
             Label(p, 520, 500 - y, 10, (255, 255, 0, 255), self.batch, g(2))] if
            p != "None" else None
            for p, y in zip(P.combination[:3] + [P.combination[-1]], (0, 65, 130, 250))
        ]
        self.arrows = [
            Triangle(465, 485 - y, 465, 465 - y, 483, 475 - y, (255, 255, 255),
                     self.batch, g(1)) for y in (0, 65, 130, 250)
        ]
        self.sprites += [
            Circle(474, 310 - y, 4, (255, 255, 255), self.batch, g(1))
            for y in range(0, 60, 20)
        ]
        self.tower_info_label.y -= 60
        self.tower_info.y -= 60





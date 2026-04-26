import pyglet as py
from dataclasses import dataclass, field
from announcements import Announcement
from window_objects import Mouse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from panels import MainPanel, TopPanel
    from game_elements import Track


defaults = {"gold": 500, "lives": 200, "wave": 0, "game_speed": 10}
protein_defaults = {}

@dataclass
class GameAttrs:
    gold: int
    lives: int
    wave: int
    game_speed: int
    paused: bool = False
    quit: bool = False
    auto: bool = False
    round_active: bool = False
    mouse: Mouse = Mouse()
    batch: py.graphics.Batch = py.graphics.Batch()
    enemies: list = field(default_factory=list)
    projectiles: list = field(default_factory=list)
    placed_towers: list = field(default_factory=list)
    enemy_classes: dict = field(default_factory=dict)
    shop_towers: dict[str] = field(default_factory=dict)
    proteins: dict[str] = field(default_factory=dict)
    main_panel: "MainPanel" = None
    top_panel: "TopPanel" = None
    track: "Track" = None
    announcement: Announcement = Announcement(batch, announcements_on=True)
    current_screen = "TitleScreen"

    def set_defaults(self):
        for key, value in defaults.items():
            setattr(self, key, value)
        for name, attrs in protein_defaults.items():
            self.proteins[name].load_data(**attrs)
        self.enemies.clear()
        self.placed_towers.clear()
        self.shop_towers.clear()
        self.shop_towers.update({
            name: protein for name, protein in self.proteins.items() if protein.shop
        })

    def lock_defaults(self):
        keys = ("number", "unlocked")
        for name, protein in self.proteins.items():
            protein_defaults[name] = {key: getattr(protein, key) for key in keys}


game_attrs = GameAttrs(**defaults)

__all__ = [game_attrs]


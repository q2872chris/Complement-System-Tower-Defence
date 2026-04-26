from abc import ABC
import random as ra
import numpy as np
from protein_towers.protein_full_bases import BasicTower
from protein_towers.panels import BlankPanel
from utilities import extend
from globals import game_attrs


class MovingGhostTower(BasicTower, ABC):
    """A tower without an upgrades section."""
    panel = BlankPanel

    def __init__(self, x: int, y: int, vec: np.array, rotation: (float | str),
                 func=lambda: None):
        super().__init__(x, y)
        self.ghost_flag = True  # For detecting this type of tower
        self.time = 0
        self.max_time = ra.randint(80, 120)
        self.rotate = rotation == "rotate"
        if not self.rotate:
            self.rotation = rotation
        self.sprite_opacity_reduction = self.sprite.opacity / self.max_time
        self.label_opacity = self.label.color[3]
        self.label_opacity_reduction = self.label_opacity / self.max_time
        self.func = func
        self.speed_modifier = 40
        self.vec = vec * self.speed_modifier * (1 + ra.random() / 5)
        self.active = False

    @extend
    def update(self, dt: float):
        if self.rotate:
            self.rotation += 1
        self.time += 1
        self.sprite.opacity -= self.sprite_opacity_reduction
        self.label_opacity -= self.label_opacity_reduction
        self.label.color = (*self.label.color[:3], int(self.label_opacity))
        vec = self.vec * dt
        self.sprite.update_position(vec)
        self.label.update_position(vec)
        if self.time == self.max_time:
            self.func()
            game_attrs.placed_towers.remove(self)



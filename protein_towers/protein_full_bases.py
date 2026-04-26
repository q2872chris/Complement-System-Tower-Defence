import pyglet as py
import numpy as np
import random as ra
from abc import ABC, abstractmethod
from globals import game_attrs
from drawables import Circle
from projectiles import Spikes
from protein_towers.protein_bases import BaseProtein, TowerBase
from .panels import UpgradablePanel, CleavablePanel, \
    SelfActivatablePanel, ActivatablePanel, C3aBackupTowerPanel, \
    AntibodyTowerPanel, StaticGhostTowerPanel, OverclockTowerPanel, \
    RadialShotTowerPanel, ManualSpikeTowerPanel
from utilities import extend, CustomComplex

g = py.graphics.OrderedGroup


class BasicTower(BaseProtein, TowerBase, ABC):
    """A full tower object that can be inherited from."""
    panel = UpgradablePanel

    def activate_panel(self, previous_panel) -> UpgradablePanel:
        return self.panel(self, previous_panel)


class CleavableTower(BasicTower, ABC):
    panel = CleavablePanel


class ActivatableTower(BasicTower, ABC):
    panel = ActivatablePanel

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.active = False


class SelfActivatableTower(ActivatableTower, ABC):
    panel = SelfActivatablePanel


class StaticGhostTower(BasicTower, ABC):
    panel = StaticGhostTowerPanel

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.sell_cost = 0
        self.time = 0
        self.max_time = np.random.randint(500, 700)
        self.sprite.opacity = 220
        self.opacity_reduction = self.sprite.opacity / self.max_time

    @extend
    def update(self, dt: float):
        if game_attrs.enemies:
            self.time += 1
            self.sprite.opacity -= self.opacity_reduction
            if self.time == self.max_time:
                game_attrs.placed_towers.remove(self)


class MultiShotTower(BasicTower, ABC):
    def spawn_projectile(self, vec: np.array):
        z = CustomComplex(*vec)
        v1 = np.array([*z.rotate(0.5)])
        v2 = np.array([*z.rotate(-0.5)])
        xy = np.array([self.x, self.y])
        positions = [xy, xy - v1 * 0.05, xy - v2 * 0.05]
        for v, (x, y) in zip((vec, v1, v2), positions):
            self.projectile_generator(x, y, v)


class RadialShotTower(BasicTower, ABC):
    panel = RadialShotTowerPanel
    upgrade_keys = ("range", "reload_time", "radial_vecs", "damage")
    radial_vecs = 8

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.upgrade_costs = [15, 30, 50, 70]
        self.upgrade_values = (10, -1, 4, 1)
        self.bullet_lifespan /= 4
        self.reload_time *= 2

    def spawn_projectile(self, _vec: np.array):
        angles = np.linspace(0, 2 * np.pi, self.radial_vecs, endpoint=False)
        vecs = np.stack((np.cos(angles), np.sin(angles)), axis=1) * self.bullet_speed
        for vec in vecs:
            self.projectile_generator(self.x, self.y, vec)

    @extend
    def update(self, dt: float):
        self.sprite.update(rotation=0)


class SniperTower(BasicTower, ABC):
    upgrade_keys = ("range", "reload_time", "bullet_speed", "damage")

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.upgrade_costs = [10, 30, 25, 70]
        self.upgrade_values = (30, -1, 50, 1)
        self.bullet_speed *= 2
        self.bullet_lifespan += 100

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        cls.range += 150


class PiercingTower(BasicTower, ABC):
    upgrade_keys = ("range", "reload_time", "pierce", "damage")

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.upgrade_costs = [10, 30, 40, 70]
        self.upgrade_values = (10, -1, 1, 1)


class GlueTower(BasicTower, ABC):
    upgrade_keys = ("range", "reload_time", "glue_strength", "duration")
    glue_strength = 2
    duration = 400

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.upgrade_costs = [10, 30, 20, 15]
        self.upgrade_values = (10, -1, 1, 50)
        self.reload_time *= 2

    @extend
    def projectile_generator(self, x, y, vec: np.array):
        game_attrs.projectiles[-1].speed_modifier = 1 / self.glue_strength


class PoisonTower(BasicTower, ABC):
    upgrade_keys = ("range", "reload_time", "poison_damage", "duration")
    poison_damage = 1
    duration = 400

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.upgrade_costs = [10, 30, 20, 15]
        self.upgrade_values = (10, -1, 1, 50)
        self.reload_time *= 2

    @extend
    def projectile_generator(self, x, y, vec: np.array):
        game_attrs.projectiles[-1].damage_tick = self.poison_damage / 100


class EngineerTower(BasicTower, ABC):
    upgrade_keys = ("range", "reload_time", "sentries", "sentry_damage")
    sentries = 1
    sentry_damage = 1

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.upgrade_costs = [10, 30, 50, 80]
        self.upgrade_values = (10, -1, 1, 1)


class SpikeTower(BasicTower, ABC):
    upgrade_keys = ("range", "reload_time", "spikes", "spike_lifespan")
    spikes = 3
    spike_lifespan = 200

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.upgrade_costs = [10, 30, 40, 15]
        self.upgrade_values = (10, -1, 1, 50)
        self.reload_time *= 2
        self.bullet_speed /= 2

    def shoot(self):
        spots = [point for point in game_attrs.track.mesh if point in self.circle]
        if spots and game_attrs.enemies:
            ind = ra.randint(0, len(spots) - 1)
            spot = spots[ind]
            theta = np.random.uniform(0, 2 * np.pi)
            spot += np.array([np.cos(theta), np.sin(theta)]) * 2
            vec = (spot - [self.x, self.y])
            vec /= np.linalg.norm(vec)
            vec *= self.bullet_speed
            game_attrs.projectiles.append(
                Spikes(self.x, self.y, 8, 3, self.spikes, (100, 100, 100),
                       vec, spot, self)
            )
            self.wait = 1


class PowerUpTower(BasicTower, ABC):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.powerup_maxcooldown = 400
        self.powerup_cooldown = 0

    @extend
    def update(self, dt: float):
        if self.powerup_cooldown > 0 and game_attrs.enemies:
            self.powerup_cooldown += 1
        if self.powerup_cooldown == self.powerup_maxcooldown:
            self.powerup_cooldown = 0

    @abstractmethod
    def powerup(self):
        pass


class OverclockTower(PowerUpTower, ABC):
    panel = OverclockTowerPanel
    upgrade_keys = ("range", "reload_time", "aura_speed", "cooldown")
    aura_speed = 13
    cooldown = 600
    power_ups = ["Overclock"]

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.upgrade_costs = [10, 30, 40, 35]
        self.upgrade_values = (10, -1, 1, -50)
        self.powerup_maxcooldown = self.cooldown

    @extend
    def update(self, dt: float):
        self.powerup_maxcooldown = self.cooldown

    def powerup(self):
        print("ahh")


class ManualSpikeTower(PowerUpTower, ABC):
    panel = ManualSpikeTowerPanel
    upgrade_keys = ("range", "reload_time", "spikes", "spike_lifespan")
    spikes = 3
    spike_lifespan = 300
    power_ups = ["Spike pile"]

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.upgrade_costs = [10, 30, 20, 10]
        self.upgrade_values = (10, -1, 1, 50)
        self.powerup_maxcooldown = 300
        self.pile = None
        self.flag = False

    @extend
    def update(self, dt: float):
        if self.pile is not None:
            self.pile.update(*game_attrs.mouse.pos())
            if any(game_attrs.mouse.pos() in piece for piece in game_attrs.track.inner_sprites):
                self.flag = True
                self.pile.color = (0, 255, 0)
            else:
                self.flag = False
                self.pile.color = (255, 0, 0)
            if game_attrs.mouse.click and self.flag:
                game_attrs.projectiles.append(
                    Spikes(game_attrs.mouse.x, game_attrs.mouse.y, 8, 3, self.spikes,
                           (100, 100, 100), None, None, self)
                )
                game_attrs.projectiles[-1].moving = False
                self.pile.delete()
                self.pile = None
                self.flag = False

    def powerup(self):
        self.pile = Circle(game_attrs.mouse.x, game_attrs.mouse.y, 40,
                           (255, 0, 0), game_attrs.batch, g(7), opacity=100)


class AntibodyTower(PowerUpTower, ABC):
    panel = AntibodyTowerPanel
    upgrade_keys = ("range", "reload_time", "antibody_damage", "damage")
    antibody_damage = 1
    power_ups = ["Antibody bomb"]

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.upgrade_costs = [10, 30, 50, 70]
        self.upgrade_values = (10, -1, 1, 1)
        self.antibody = None

    @extend
    def update(self, dt: float):
        if self.antibody is not None:
            self.antibody.update(*game_attrs.mouse.pos())
            if game_attrs.mouse.click:
                for enemy in game_attrs.enemies:
                    if enemy.position in self.antibody:
                        enemy.health -= self.antibody_damage
                self.antibody.delete()
                self.antibody = None

    def powerup(self):
        self.antibody = Circle(game_attrs.mouse.x, game_attrs.mouse.y, 90,
                               (0, 255, 255), game_attrs.batch, g(7), opacity=100)


class C3aBackupTower(PowerUpTower, ABC):
    panel = C3aBackupTowerPanel
    upgrade_keys = ("range", "reload_time", "C3a_count", "damage")
    C3a_count = 1
    power_ups = ["C3a backup"]

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.upgrade_costs = [10, 30, 20, 70]
        self.upgrade_values = (10, -1, 1, 1)

    def powerup(self):
        angles = np.linspace(0, 2 * np.pi, self.C3a_count + 1)
        rand_angles = np.random.uniform(angles[:-1], angles[1:])
        locations = np.stack((np.cos(rand_angles), np.sin(rand_angles)), axis=-1)
        locations *= np.random.randint(70, 90, 1)
        locations += [[self.x, self.y]]
        for location in locations:
            game_attrs.placed_towers.append(
                type("Temp C3a", (game_attrs.proteins["C3a"], StaticGhostTower),
                     {"shop": 0})(*location)
            )



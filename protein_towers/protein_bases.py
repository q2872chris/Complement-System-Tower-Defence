import pyglet as py
from abc import ABC
from drawables import Sprite, Circle, Label
from utilities import image_cutter, quadratic_solver
import game_elements  # Don't import MovingGhostTower directly, avoids circular imports
import numpy as np
from globals import game_attrs
from projectiles import Projectile
from enemies import EnemyBase

cut_image = image_cutter(r"images\sprites.png")
g = py.graphics.OrderedGroup


class ProteinTowerBase(ABC):
    img: py.image.ImageDataRegion = None
    camo_aura = False
    self_camo = False


class TowerBase(ProteinTowerBase, ABC):
    colour = (0, 0, 0)
    cost = 0
    range = 0
    reload_time = 0
    bullet_lifespan = 0
    damage = 0
    bullet_speed = 300
    pierce = 1
    upgrade_costs = (0, 0, 0, 0)
    upgrade_values = (10, -1, 10, 1)
    upgrade_keys = ("range", "reload_time", "bullet_lifespan", "damage")
    sell_modifier = 0.9
    upgrade_cost_modifier = 1.3
    activatable = False
    self_activate = False

    def __init__(self, x: int, y: int):
        cls = type(self)
        self.name = type(self).__name__
        self.x = x
        self.y = y
        # Rendering levels need to be changed
        self.circle = Circle(x, y, self.range, self.colour, game_attrs.batch, g(3), 140)
        self.circle.hide()
        self.sprite = Sprite(self.img, x, y, game_attrs.batch, g(4))
        self.label = Label(self.name, x, y + self.sprite.width / 2 + 5,
                           8, (255, 255, 0, 255), game_attrs.batch, g(4))
        self.sell_cost = int(self.cost * self.sell_modifier)
        self.wait = 0
        self.rotation = 0
        self.range = cls.range
        self.reload_time = cls.reload_time
        self.bullet_lifespan = cls.bullet_lifespan
        self.damage = cls.damage
        self.upgrade_costs = list(self.upgrade_costs)
        self.upgrade_nums = [0] * len(self.upgrade_keys)
        self.floating_tower = None
        self.target_mode = "First"
        self.pop_count = 0
        self.active = True
        if self.activatable or self.self_activate:
            self.sprite.opacity = 180

    def upgrade(self, ind: int):
        self.sell_cost = int(self.sell_cost + self.upgrade_costs[ind] * self.sell_modifier)
        self.upgrade_costs[ind] = int(self.upgrade_costs[ind] * self.upgrade_cost_modifier)
        self.upgrade_nums[ind] += 1
        attr = getattr(self, key := self.upgrade_keys[ind])
        setattr(self, key, attr + self.upgrade_values[ind])

    def __del__(self):
        self.label.delete()

    def split(self, ids: list, static=False):
        if not static:
            angles = np.linspace(0, 2 * np.pi, len(ids) + 1)
            rand_angles = np.random.uniform(angles[:-1], angles[1:])
            trajectories = np.stack((np.cos(rand_angles), np.sin(rand_angles)), axis=-1)
            directions = -np.degrees(rand_angles)
        else:
            trajectories = np.zeros((len(ids), 2))
            directions = ["rotate"] * len(ids)
        for tower_id, trajectory, direction in zip(ids, trajectories, directions):
            protein = game_attrs.proteins[tower_id]
            new_object = type(protein.__name__,
                              (game_elements.MovingGhostTower,),
                              dict(protein.__dict__) | {"shop": 0})
            game_attrs.placed_towers.append(new_object(self.x, self.y, trajectory, direction,
                                                       self.ghost_func(protein)))

    @staticmethod
    def ghost_func(protein):
        def inner():
            protein.update_count(1)
        return inner

    def update(self, dt: float):
        if self.circle.radius != self.range:
            self.circle.radius = self.range
        self.sprite.update(rotation=self.rotation)
        self.move_tower()
        if self.wait == 0 and self.active:
            self.shoot()
        elif self.wait < self.reload_time:
            self.wait += 1
        else:
            self.wait = 0

    def get_enemies(self) -> list[EnemyBase]:
        # Use shared lists?
        match self.target_mode:
            case "Last":
                return sorted(game_attrs.enemies, key=lambda x: x.progress)
            case "Strong":
                return sorted(game_attrs.enemies, key=lambda x: (x.full_health, x.progress),
                              reverse=True)
            case "Weak":
                return sorted(game_attrs.enemies, key=lambda x: (x.full_health, x.progress))
            case _:   # First
                return sorted(game_attrs.enemies, key=lambda x: x.progress, reverse=True)

    def shoot(self):
        for enemy in self.get_enemies():
            # self_camo and camo_aura:
            if enemy.camo and not self.self_camo and not \
                    any((self.x, self.y) in tower.circle for tower in
                        set(game_attrs.placed_towers) - {self} if tower.camo_aura):
                continue
            if any(point in self.circle for point in enemy.get_points()):
                vec = np.array(enemy.position, dtype=float) - [self.x, self.y]
                vec /= np.linalg.norm(vec)
                vec *= self.bullet_speed
                vec = self.smart_shoot(
                    np.array([self.x, self.y]), enemy.position, enemy.vec,
                    self.bullet_speed, vec
                )
                self.rotation = -np.degrees(np.math.atan2(vec[1], vec[0]))
                self.spawn_projectile(vec)
                self.wait = 1
                break

    @staticmethod
    def smart_shoot(p_t, p_e, v_e, s_b, vec) -> np.array:
        r = p_e - p_t
        a = np.dot(v_e, v_e) - s_b ** 2
        b = 2 * np.dot(r, v_e)
        c = np.dot(r, r)
        ts = quadratic_solver(a, b, c)
        if ts is None:
            return vec
        ts = [t for t in ts if t > 0]
        if not ts:
            return vec
        return v_e + (p_e - p_t) / min(ts)

    def spawn_projectile(self, vec: np.array):
        """To be utilised by subclasses with polymorphism."""
        self.projectile_generator(self.x, self.y, vec)

    def projectile_generator(self, x, y, vec: np.array):
        game_attrs.projectiles.append(Projectile(x, y, 2, (0, 0, 0), vec, self))

    def move_tower(self):
        if self.floating_tower is not None and self.floating_tower.active:
            self.floating_tower.run()
        elif self.floating_tower is not None:
            self.sprite.opacity = 255
            if self.floating_tower.placement:
                game_attrs.placed_towers.remove(self)
            game_attrs.mouse.release_focus("move_tower")
            self.floating_tower = None


class BaseProtein(ProteinTowerBase, ABC):
    unlocked = False
    shop = False
    cut: tuple[int, int] = NotImplemented
    width = 0
    height = 0
    number = 0
    info = ""
    game_info = ""
    base = []
    combination = []
    self_cleave = []
    cleave = []
    components = []
    slow = False
    uncamo = False
    power_ups = []
    abilities = []
    sprite: Sprite = None
    count_label: Label = None

    def __init_subclass__(cls, **kwargs):
        if cls.cut is not NotImplemented:
            cls.img = cut_image(*cls.cut, cls.width, cls.height)
            if cls.shop:
                cls.sprite = Sprite(cls.img, 0, 0, game_attrs.batch, g(3))
                cls.count_label = Label(str(cls.number), 0, 0, 9, (255, 255, 255, 255),
                                        game_attrs.batch, g(3))
                if not cls.unlocked:
                    cls.sprite.hide()
                    cls.count_label.hide()
            cls.abilities = []
            abilities = {"slow": "slowing aura", "self_camo": "sees camo",
                         "uncamo": "can de-camo", "camo_aura": "camo aura"}
            for key, value in abilities.items():
                if getattr(cls, key):
                    cls.abilities.append(value)

    @classmethod
    def load_data(cls, **kwargs):
        for key, value in kwargs.items():
            setattr(cls, key, value)
        if cls.shop:
            if cls.unlocked:
                cls.sprite.show()
                cls.count_label.show()
            else:
                cls.sprite.hide()
                cls.count_label.hide()
            cls.count_label.text = str(cls.number)

    @classmethod
    def update_count(cls, num):
        if cls.shop:
            cls.number += num
            cls.count_label.text = str(cls.number)








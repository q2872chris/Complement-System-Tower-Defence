import pyglet as py
from abc import ABC
from drawables import Sprite, Label, Circle
from utilities import image_cutter, extend
from globals import game_attrs
import numpy as np

cut_image = image_cutter(r"images\sprites.png")
g = py.graphics.OrderedGroup


class EnemyBase(Sprite, ABC):
    img: py.image.ImageDataRegion = None
    cut = (0, 0)
    width = 0
    height = 0
    tag: str = NotImplemented
    speed = 0
    damage = 0
    full_damage = 0
    max_health = 0
    full_health = 0   # Used for targeting strong
    value = 0
    full_value = 0
    bases = []
    upper = []
    slow_immune = False
    info = ""
    points = []
    vecs = []

    @classmethod
    def walk_bases(cls, key: str):
        attr = getattr(cls, key)
        if cls.bases:
            return attr + \
                sum(game_attrs.enemy_classes[base].walk_bases(key) for base in cls.bases)
        return attr

    @classmethod
    def initialise(cls):
        cls.full_health = cls.walk_bases("max_health")
        cls.full_value = cls.walk_bases("value")
        cls.damage = cls.max_health
        cls.full_damage = cls.full_health
        cls.points = np.array(game_attrs.track.points)
        vecs = cls.points[1:] - cls.points[:-1]
        cls.vecs = vecs / np.linalg.norm(vecs, axis=1).reshape(15, 1)

    def __init_subclass__(cls, **kwargs):
        if cls.tag is not NotImplemented:
            cls.img = cut_image(*cls.cut, cls.width, cls.height)

    def __init__(self, x: int, y: int, last_point=0, health_modifier=0,
                 progress=0.0, camo=False, regen=False, optional_id=0, z=3):
        cls = type(self)
        super().__init__(cls.img, x, y, game_attrs.batch, g(z), scale=0.9,
                         opacity=(150 if camo else 255))
        self.progress = progress
        self.last_point = last_point
        self.vec = np.array([0, 0])    # For tower aiming
        self.health = cls.max_health + health_modifier
        self.full_health = cls.full_health + health_modifier
        self.optional_id = Label(str(optional_id), x, y, 12, (0, 255, 255, 255),
                                 game_attrs.batch, g(z + 1))
        self.drawables = [self.optional_id]
        self.id = id(self)
        self.camo = camo
        self.regen = regen
        self.regen_max_wait = 100
        self.regen_wait = 0
        self.upper_list = []
        self.speed_modifier = 1
        self.damage_tick = 0
        self.effect_cooldown = 0
        self.effect_maxcooldown = 300

    def spawn_bases(self):
        n = len(self.bases)
        steps = np.arange(-n + 1, n, 2) / 15
        for base, step in zip(self.bases, steps):
            new_enemy = game_attrs.enemy_classes[base](
                self.x, self.y, self.last_point, self.health, self.progress,
                self.camo, self.regen, self.optional_id.text
            )
            if step != 0:
                new_enemy.movement(step)
            self.set_new_enemy_attrs(new_enemy)

    def set_new_enemy_attrs(self, new_enemy, upper=False):
        new_enemy.vec = self.vec
        new_enemy.id = self.id
        new_enemy.regen_wait = self.regen_wait
        new_enemy.effect_cooldown = self.effect_cooldown
        new_enemy.speed_modifier = self.speed_modifier
        new_enemy.damage_tick = self.damage_tick
        if self.regen and upper:
            new_enemy.upper_list = self.upper_list
        elif self.regen:
            new_enemy.upper_list = self.upper_list + [self.tag]
        game_attrs.enemies.append(new_enemy)

    def move(self, vec: np.array):
        self.progress += np.linalg.norm(vec)
        self.update_position(vec)
        for i in self.drawables:
            i.update_position(vec)

    def set_pos(self, pos: list[int]):
        self.progress += np.linalg.norm(np.array(self.position) - pos)
        self.update(*pos)
        for i in self.drawables:
            i.update(*pos)

    def movement(self, dt: float):
        self.vec = self.vecs[self.last_point] * self.speed * game_attrs.game_speed * \
                   self.speed_modifier
        if not self.slow_immune:
            for tower in game_attrs.placed_towers:   # Eg ice towers
                if self.position in tower.circle and tower.slow:
                    self.vec /= 2
                    break
        vec = self.vec * dt
        last_point = self.points[self.last_point]
        next_point = self.points[self.last_point + 1]
        if np.dot(next_point - self.position - vec, vec) <= 0 < \
                np.dot(next_point - self.position, vec):
            self.set_pos(next_point)
            self.last_point += 1
        elif np.dot(next_point - self.position, vec) < 0:
            if np.dot(last_point - self.position - vec, vec) <= 0:
                self.set_pos(last_point)
            elif tuple(last_point) == tuple(self.position):
                self.last_point -= 1
        else:
            self.move(vec)
        self.run_actions()   # The update function

    def __del__(self):
        self.delete()
        for i in self.drawables:
            i.delete()

    def run_actions(self):
        self.health -= self.damage_tick
        if self.effect_cooldown > 0:
            self.effect_cooldown += 1
        if self.effect_cooldown == self.effect_maxcooldown:
            self.effect_cooldown = 0
            self.damage_tick = 0
            self.speed_modifier = 1
        if self.regen:
            self.regen_wait += 1
            if self.regen_wait == self.regen_max_wait:
                self.regen_wait = 0
                if self.health < self.max_health:
                    self.health += 1
                elif self.upper_list:
                    self.health = 0
                    next_upper = self.upper_list.pop(-1)
                    new_enemy = game_attrs.enemy_classes[next_upper](
                        self.x, self.y, self.last_point, self.health, self.progress,
                        self.camo, self.regen, self.optional_id.text
                    )
                    self.set_new_enemy_attrs(new_enemy, upper=True)
                    game_attrs.enemies.remove(self)


class Vaccinia(EnemyBase, ABC):
    tag = 'v'

    def __init__(self, x: int, y: int, last_point=0, health_modifier=0,
                 progress=0.0, camo=False, regen=False, optional_id=0, z=3):
        super().__init__(x, y, last_point, health_modifier, progress,
                         camo, regen, optional_id, z)
        self.circle = Circle(x, y, 55, (255, 255, 255),
                             game_attrs.batch, g(4), opacity=50)
        self.drawables += [self.circle]

    @extend
    def run_actions(self):   # Disables towers
        for tower in game_attrs.placed_towers:
            if (tower.x, tower.y) in self.circle:
                tower.wait = 1


classes = [Vaccinia]
injections = {cls.tag: cls for cls in classes}


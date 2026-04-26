import pyglet as py
from drawables import Circle, Star
from globals import game_attrs
import numpy as np
import random as ra

g = py.graphics.OrderedGroup


class Projectile(Circle):
    def __init__(self, x: int, y: int, radius: int, colour: tuple[int, int, int],
                 vec: np.array, tower):
        super().__init__(x, y, radius, colour, game_attrs.batch, g(4))
        self.tower = tower
        self.vec = vec
        self.wait = 0
        self.damage = tower.damage
        self.lifespan = tower.bullet_lifespan
        self.uncamo = tower.uncamo
        self.pierce = tower.pierce
        self.pierce_list: list[int] = []
        self.speed_modifier = 1
        self.damage_tick = 0

    def run(self, dt: float):
        self.wait += 1
        if self.wait == self.lifespan or \
                self.position not in game_attrs.main_panel.panel:
            game_attrs.projectiles.remove(self)
            return
        self.update_position(self.vec * dt)
        for enemy in game_attrs.enemies:
            if self.position in enemy and enemy.id not in self.pierce_list:
                self.pierce -= 1
                self.pierce_list.append(enemy.id)
                enemy.health -= self.damage
                enemy.damage_tick = self.damage_tick
                enemy.speed_modifier = self.speed_modifier
                enemy.effect_cooldown = 1
                if self.uncamo:
                    enemy.camo = False
                if enemy.health < 1:
                    self.tower.pop_count += 1
                if self.pierce == 0:
                    game_attrs.projectiles.remove(self)
                    return
                break


class Spikes:
    def __init__(self, x: int, y: int, outer_radius: int, inner_radius: int,
                 num_spikes: int, colour: tuple[int, int, int], vec: np.array,
                 end_point, tower):
        if num_spikes == 1:
            self.star = Circle(x, y, inner_radius, colour, game_attrs.batch, g(4))
        else:
            self.star = Star(x, y, outer_radius, inner_radius, num_spikes, colour,
                             ra.randint(0, 359), game_attrs.batch, g(4))
        self.tower = tower
        self.pos = (x, y)
        self.vec = vec
        self.end_point = end_point
        self.moving = True
        self.wait = 0
        self.damage = tower.damage
        self.lifespan = tower.spike_lifespan

    def run(self, dt: float):
        if self.moving:
            vec = self.vec * dt
            if np.dot(self.end_point - np.array(self.star.position) - vec, vec) <= 0:
                self.star.position = self.end_point
                self.moving = False
            else:
                self.star.update_position(vec)
        elif game_attrs.enemies:
            self.wait += 1
            if self.wait == self.lifespan or \
                    self.star.position not in game_attrs.main_panel.panel:
                game_attrs.projectiles.remove(self)
                return
        for enemy in game_attrs.enemies:
            if self.star.position in enemy:
                enemy.health -= self.damage
                if enemy.health < 1:
                    self.tower.pop_count += 1
                if hasattr(self.star, "num_spikes"):
                    new_spike = Spikes(
                        self.star.x, self.star.y, 8, 3, self.star.num_spikes - 1,
                        (100, 100, 100), self.vec, self.end_point, self.tower
                    )
                    new_spike.moving = self.moving
                    game_attrs.projectiles.append(new_spike)
                game_attrs.projectiles.remove(self)
                return


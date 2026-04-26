from .enemies import EnemyBase
from globals import game_attrs
from pyglet.window import key

with open("enemies/waves") as reader:
    waves = [line.strip() for line in reader.readlines()]


class EnemyController:
    def __init__(self):
        self.enemies: list[EnemyBase] = game_attrs.enemies
        self.points = game_attrs.track.points
        self.current_wave_index = 0
        self.current_wave = waves[0]
        self.read_position = 0
        self.wait = 0
        self.max_wait = 20
        self.end_round_func = lambda: None   # To be initialised by GameScreen
        self.enemies_total = 0
        self.manual_camo = False
        self.manual_regen = False

    def update(self, dt: float):
        if self.wait == self.max_wait:
            self.wait = 0
        if game_attrs.round_active and self.wait == 0:
            self.spawn_new_enemy()
        self.update_enemies(dt)
        self.wait += 1

    def reset(self, new_round=0):
        self.wait = 0
        self.read_position = 0
        self.current_wave_index = new_round
        self.current_wave = waves[self.current_wave_index]

    def spawn_new_enemy(self, camo=False, regen=False):
        new = self.current_wave[self.read_position]
        if new == 's':
            game_attrs.game_speed += 3
        elif new == 'i':
            self.max_wait -= 2
        elif new == 'c':
            camo = True
        elif new == 'r':
            regen = True
        elif new != '0':
            self.enemies_total += 1
            new_enemy = game_attrs.enemy_classes[new](
                *self.points[0], camo=camo, regen=regen, optional_id=self.enemies_total
            )
            self.enemies.append(new_enemy)
        self.read_position += 1
        self.check_wave()
        if new in ('s', 'i', 'c', 'r') and game_attrs.round_active:
            self.spawn_new_enemy(camo, regen)

    def check_wave(self):
        if self.read_position == len(self.current_wave):
            self.enemies_total = 0
            game_attrs.round_active = False
            self.end_round_func()
            self.read_position = 0
            self.current_wave_index += 1
            self.current_wave = waves[self.current_wave_index]
            if game_attrs.auto:
                game_attrs.wave += 1
                game_attrs.round_active = True

    def update_enemies(self, dt: float):
        for enemy in self.enemies:
            if enemy.health < 1:
                game_attrs.gold += enemy.value
                if enemy.bases:
                    enemy.spawn_bases()
                self.enemies.remove(enemy)
            elif enemy.last_point == len(self.points) - 1:
                self.enemies.remove(enemy)
                game_attrs.lives -= enemy.full_damage
            else:
                enemy.movement(dt)

    def on_key_press(self, symbol: int, _modifiers: int):
        advanced_enemies = [i.upper() for i in game_attrs.enemy_classes.keys()
                            if i.isalpha()]
        keys = {getattr(key, i): i for i in advanced_enemies}
        if game_attrs.current_screen == "GameScreen":
            if symbol == key.C:
                self.manual_camo = True
            if symbol == key.R:
                self.manual_regen = True
            if symbol in keys:
                self.enemies.append(
                    game_attrs.enemy_classes[keys[symbol].lower()](
                        *self.points[0], camo=self.manual_camo, regen=self.manual_regen
                    )
                )
            elif 48 <= symbol <= 57:
                self.enemies.append(
                    game_attrs.enemy_classes[str(symbol - 47)](
                        *self.points[0], camo=self.manual_camo, regen=self.manual_regen
                    )
                )
            elif symbol == key.M:
                for i in self.enemies:
                    i.health -= 1
            elif symbol == key.S:
                game_attrs.game_speed += 3

    def on_key_release(self, symbol: int, _modifiers: int):
        if game_attrs.current_screen == "GameScreen":
            if symbol == key.C:
                self.manual_camo = False
            if symbol == key.R:
                self.manual_regen = False

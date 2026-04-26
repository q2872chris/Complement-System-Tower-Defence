import pyglet as py
from drawables import Sprite, Circle
from globals import game_attrs
from utilities import extend

g = py.graphics.OrderedGroup


class FloatingTowerShop:
    def __init__(self, tower, drag=False, clicked=False):
        self.top_panel = game_attrs.top_panel
        self.main_panel = game_attrs.main_panel
        self.track = game_attrs.track
        self.shop_towers = game_attrs.shop_towers
        self.placed_towers = game_attrs.placed_towers
        self.proteins = game_attrs.proteins
        self.mouse = game_attrs.mouse
        self.tower = tower
        self.sprite = Sprite(tower.img, 0, 0, game_attrs.batch, g(6))
        self.radius = Circle(0, 0, self.tower.range, (0, 0, 0),
                             game_attrs.batch, g(5), opacity=100)
        self.colour_flag = "invalid"
        self.target_tower = None
        self.drag = drag
        self.clicked = clicked
        self.active = True

    def update(self, x, y, colour_flag="invalid"):
        self.sprite.update(x, y)
        self.radius.x = x
        self.radius.y = y
        self.colour_flag = colour_flag
        match colour_flag:
            case "valid":
                self.radius.color = (0, 255, 0)
            case "combine":
                self.radius.color = (0, 0, 255)
            case "cleave":
                self.radius.color = (255, 255, 0)
            case "full_cleave":
                self.radius.color = (255, 255, 0)
            case "activate":
                self.radius.color = (255, 0, 255)
            case _:
                self.radius.color = (255, 0, 0)

    def get_combination(self):
        ind = self.tower.base.index(self.target_tower.name)
        return self.tower.combination[ind]

    def get_cleave(self):
        try:
            ind = self.tower.base.index(self.target_tower.name)
            return self.tower.cleave[ind]
        except IndexError:
            return []

    def track_collide(self) -> bool:
        return any(point in piece for piece in self.track.outer_sprites
                   for point in self.sprite.get_points(grid=3))

    def tower_collide(self, tower) -> bool:
        return any(point in tower.sprite for point in self.sprite.get_points())

    def run(self):
        self.floating_tower_collision()
        if (self.mouse.click and self.clicked) or (not self.mouse.click and self.drag):
            if self.tower.shop:
                self.tower.sprite.show()
                self.tower.count_label.show()
            self.place_tower()
            self.radius.delete()
            self.sprite.delete()
            self.active = False

    def get_placed_towers(self):
        return [tower for tower in self.placed_towers if not hasattr(tower, "ghost_flag")]

    def floating_tower_collision(self):
        collides = [tower for tower in self.get_placed_towers() if self.tower_collide(tower)]
        combines = [tower for tower in collides if tower.name in self.tower.base]
        self.top_panel.update_text(self.tower)
        if combines:
            self.target_tower = target = combines[0]
            combination_name = self.get_combination()
            if combination_name.lower() == "none" or combination_name == target.name:
                cleave_names = self.get_cleave()
                if combination_name.lower() == "none":
                    self.update(*self.mouse.pos(), "full_cleave")
                    cleave_names = self.get_cleave()
                else:
                    self.update(*self.mouse.pos(), "cleave")
                temp = type(" & ".join(cleave_names), (),
                            {"cost": self.tower.cost, "show_base": ""})
                self.top_panel.update_text(temp)
            else:
                self.update(*self.mouse.pos(), "combine")
                self.top_panel.update_text(self.proteins[combination_name])
        elif not self.sprite.inside_rect(self.main_panel.panel) or \
                self.track_collide() or collides:
            self.update(*self.mouse.pos())
        else:
            self.update(*self.mouse.pos(), "valid")

    def place_tower(self):
        if self.colour_flag == "valid":
            self.place_tower_default()
        elif "cleave" in self.colour_flag:
            self.instant_cleave()
        elif self.colour_flag == "combine":
            self.combine()

    def place_tower_default(self):
        self.unlock_towers(self.tower)
        new_tower = self.tower(*self.mouse.pos())
        game_attrs.placed_towers.append(new_tower)
        game_attrs.gold -= self.tower.cost
        self.tower.update_count(-1)

    def instant_cleave(self):
        game_attrs.gold -= self.tower.cost
        target = self.target_tower
        game_attrs.gold += int(target.sell_cost - target.cost * target.sell_modifier)
        target.split(self.get_cleave().copy())
        self.tower.update_count(-1)
        if self.colour_flag == "full_cleave":
            game_attrs.placed_towers.remove(target)

    def combine(self):
        combination = self.proteins[self.get_combination()]
        if game_attrs.gold >= combination.cost:
            # Instant cleaving:
            if self.tower.cleave:
                self.target_tower.split(self.get_cleave())
            self.tower.update_count(-1)
            self.unlock_towers(combination)
            new_tower = self.get_new_tower(combination)
            # Preserve upgrades at a cost:
            for ind, num in enumerate(self.target_tower.upgrade_nums):
                for _ in range(max(0, num - 1)):
                    new_tower.upgrade(ind)
            self.clear_old_tower()
            self.placed_towers.append(new_tower)
            game_attrs.gold -= combination.cost

    def get_new_tower(self, combination):
        return combination(*self.target_tower.sprite.position)

    def clear_old_tower(self):
        self.placed_towers.remove(self.target_tower)

    def unlock_towers(self, tower):
        for i in tower.unlock_towers:
            new = self.shop_towers[i]
            new.unlocked = True
            new.sprite.show()
            new.count_label.show()
            game_attrs.announcement.activate(f"{i} unlocked", once=True)


class FloatingTowerMovement(FloatingTowerShop):
    def __init__(self, old_tower):
        super().__init__(type(old_tower), clicked=True)
        self.old_tower = old_tower
        self.placement = False

    def get_cleave(self):
        """Polymorphism, override get_cleave for movement version."""
        try:
            ind = self.tower.base.index(self.target_tower.name)
            return self.tower.move_cleave[ind]
        except IndexError:
            return []

    def get_placed_towers(self):
        return set(super().get_placed_towers()) - {self.old_tower}

    @extend
    def place_tower_default(self):
        self.placement = True
        for ind, num in enumerate(self.old_tower.upgrade_nums):
            for _ in range(num):
                game_attrs.placed_towers[-1].upgrade(ind)

    @extend
    def instant_cleave(self):
        if self.colour_flag == "cleave":
            self.placement = True

    def get_new_tower(self, combination):
        if self.target_tower.name in self.old_tower.root:
            return combination(*self.old_tower.sprite.position)
        return combination(*self.target_tower.sprite.position)

    def clear_old_tower(self):
        if self.target_tower.name not in self.old_tower.root:
            self.placed_towers.remove(self.target_tower)
        if self.old_tower.name not in self.old_tower.root:
            self.placement = True







import pyglet as py
from globals import game_attrs
from screens import Typer
from sql import load_game, game_vars, protein_vars

protein_keys = list(protein_vars.keys())[1:]
g = py.graphics.OrderedGroup


class LoadScreen(Typer):
    batch = py.graphics.Batch()

    def __init__(self):
        super().__init__()
        self.alter_title_screen = lambda **kwargs: None   # To be initialised in GameController
        self.stop_funcs = [self.load]

    def load(self):
        game_info, proteins_info, towers_info, announcements_info = load_game(self.text)
        if game_info is not None:
            for key, attr in zip(game_vars.keys(), game_info):
                setattr(game_attrs, key, attr)
            for name, *attrs in proteins_info:
                game_attrs.proteins[name].load_data(**dict(zip(protein_keys, attrs)))
            game_attrs.enemies.clear()
            game_attrs.placed_towers.clear()
            for i in towers_info:
                name, x, y, *upgrade_nums = i
                tower = game_attrs.proteins[name](x, y)
                for ind, num in enumerate(upgrade_nums):
                    for _ in range(num):
                        tower.upgrade(ind)
                game_attrs.placed_towers.append(tower)
            game_attrs.announcement.previous = [i[0] for i in announcements_info]
            self.alter_title_screen(new_round=game_info[2])




import pyglet as py
from globals import game_attrs
from screens import Typer
from sql import save_game, game_vars

g = py.graphics.OrderedGroup


class SaveScreen(Typer):
    batch = py.graphics.Batch()

    def __init__(self):
        super().__init__()
        self.stop_funcs = [self.save]

    def save(self):
        game_info = [getattr(game_attrs, var) for var in game_vars.keys()]
        towers = [tower for tower in game_attrs.placed_towers
                  if not hasattr(tower, "ghost_flag")]
        towers_info = [(i.name, i.x, i.y, *i.upgrade_nums) for i in towers]
        proteins_info = [(name, i.unlocked, i.number)
                         for name, i in game_attrs.proteins.items()]
        announcements_info = game_attrs.announcement.previous
        save_game(self.text, game_info, proteins_info, towers_info, announcements_info)





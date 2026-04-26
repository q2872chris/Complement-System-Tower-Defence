import pyglet as py
from windows import Controller
from utilities import extend
from globals import game_attrs
from screens import all_screens, BaseScreen, TowerTemplateScreen, \
    EnemyTemplateScreen, extra_screens
from panels import MainPanel, TopPanel
from game_elements import Track
from protein_towers.tower_creation import get_proteins
from enemies.enemy_creation import get_enemies

g = py.graphics.OrderedGroup


class GameController(Controller):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initialise_globals_dataclass()
        self.screens_dict = {screen.__name__: screen() for screen in all_screens}
        other_screens = {
            key: type("", (TowerTemplateScreen,), {"batch": py.graphics.Batch()})
            for key in game_attrs.proteins.keys()
        }
        other_screens |= {screen.__name__: screen for screen in extra_screens}
        self.screens_dict |= {
            name: screen(game_attrs.proteins[name]) for name, screen in other_screens.items()
        }
        self.screens_dict |= {
            key: type("", (EnemyTemplateScreen,), {"batch": py.graphics.Batch()})(value)
            for key, value in game_attrs.enemy_classes.items()
        }
        self.handlers_initialisation()

    def handlers_initialisation(self):
        self.push_handlers(self.screens_dict["SaveScreen"])
        self.push_handlers(self.screens_dict["LoadScreen"])
        self.push_handlers(self.screens_dict["GameScreen"].main_panel)
        self.push_handlers(self.screens_dict["GameScreen"].enemy_controller)
        self.screens_dict["LoadScreen"].alter_title_screen = self.on_load
        self.screens_dict["TitleScreen"].on_start_new_game = self.on_load
        self.screens_dict["CheckStartScreen"].on_start_new_game = self.on_load

    def on_load(self, new_round=0):
        self.screens_dict["TitleScreen"].resume_button.show()
        game_screen = self.screens_dict["GameScreen"]
        game_screen.main_panel.switch_buttons_on_load()
        game_screen.enemy_controller.reset(new_round)
        game_attrs.round_active = False

    @staticmethod
    def initialise_globals_dataclass():
        proteins = get_proteins(pull=True)
        game_attrs.proteins.update(proteins)
        game_attrs.enemy_classes.update(get_enemies(pull=True))
        game_attrs.shop_towers.update({
            name: protein for name, protein in proteins.items() if protein.shop
        })
        game_attrs.track = Track()
        game_attrs.top_panel = TopPanel()
        game_attrs.main_panel = MainPanel()
        game_attrs.lock_defaults()
        for enemy_class in game_attrs.enemy_classes.values():
            enemy_class.initialise()

    @extend
    def update(self, dt: float):
        if game_attrs.quit:
            self.close()
        self.screens_dict[game_attrs.current_screen].update(dt)

    @extend
    def on_draw(self):
        current_screen = self.screens_dict[game_attrs.current_screen]
        if not current_screen.loaded:
            current_screen.build_sprites()
        current_screen.batch.draw()
        if game_attrs.current_screen != "GameScreen":
            BaseScreen.batch.draw()


if __name__ == "__main__":
    GameController(width=900, height=600, resizable=False, fullscreen=False,
                   caption="game_controller test")
    py.app.run()


from globals import game_attrs

# Must be defined before other imports take place
def goto_screen(screen_name: str):
    def inner():
        game_attrs.current_screen = screen_name
    return inner

from .base_screen import BaseScreen, Typer
from .game_screen import GameScreen
from .title_screen import TitleScreen
from .guide_screen import GuideScreen
from .info_screen import InfoScreen
from .credits_screen import CreditsScreen
from .load_screen import LoadScreen
from .save_screen import SaveScreen
from .check_start_screen import CheckStartScreen
from .portfolios_home_screen import PortfoliosHomeScreen
from .towers_screen import TowersScreen
from .enemies_screen import EnemiesScreen
from .tower_template_screen import TowerTemplateScreen, C9
from .enemy_template_screen import EnemyTemplateScreen


# TitleScreen must come first
all_screens = [TitleScreen, GuideScreen, InfoScreen, CheckStartScreen,
               CreditsScreen, LoadScreen, SaveScreen, GameScreen,
               PortfoliosHomeScreen, TowersScreen, EnemiesScreen]
extra_screens = [C9]




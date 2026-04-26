from enemies.enemy_information import get_data
from enemies.enemies import EnemyBase, injections


def inject_base(tag: str):
    if tag in injections:
        return injections[tag]
    return EnemyBase


def get_enemies(pull=True):
    enemy_info = get_data(pull)
    enemies = {attrs["tag"]: type(name, (inject_base(attrs["tag"]),), attrs)
               for name, attrs in enemy_info.items()}
    return enemies


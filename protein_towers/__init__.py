from .protein_full_bases import RadialShotTower, \
    MultiShotTower, SniperTower, BasicTower, PiercingTower, \
    EngineerTower, GlueTower, PoisonTower

tower_types = [RadialShotTower, MultiShotTower, SniperTower,
               PiercingTower, BasicTower, EngineerTower,
               GlueTower, PoisonTower]
tower_names = [i.__name__ for i in tower_types]
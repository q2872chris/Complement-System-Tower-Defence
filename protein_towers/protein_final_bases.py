from abc import ABC
from protein_towers.protein_full_bases import RadialShotTower, \
    MultiShotTower, SniperTower, PiercingTower, C3aBackupTower, \
    AntibodyTower, SpikeTower, ManualSpikeTower, GlueTower, PoisonTower, \
    OverclockTower, EngineerTower
from .panels import MBLPanel


class Bb(SniperTower, ABC):
    pass

class B(RadialShotTower, ABC):
    pass

class D(MultiShotTower, ABC):
    pass

class P(PiercingTower, ABC):
    pass

class C3(C3aBackupTower, ABC):
    pass

class MBL(AntibodyTower, ABC):
    pass

class C5a(SpikeTower, ABC):
    pass

class Ba(ManualSpikeTower, ABC):
    pass

class C3a(GlueTower, ABC):
    pass

class C5b(PoisonTower, ABC):
    pass

class C5(OverclockTower, ABC):
    pass

class C6(EngineerTower, ABC):
    pass

classes = [Bb, B, D, P, C3, MBL, C5a, Ba, C3a, C5b, C5, C6]
injections = {cls.__name__: cls for cls in classes}


def new_MBL(name: str, ind: int, C5b9):
    attrs = dict(C5b9.__dict__)
    attrs["range"] += 10 * (ind - 1)
    attrs["cost"] += 5 * (ind - 1)
    attrs["bullet_lifespan"] += 5 * (ind - 1)
    attrs["C9s"] = ind
    attrs["panel"] = MBLPanel
    attrs["base"] = ["C9"] if ind < 16 else []
    attrs["combination"] = [f"C5b-9({ind + 1})"] if ind < 16 else []
    # Mutable elements must be set explicitly
    attrs["components"] = attrs["components"] + ["C9"] * (ind - 1)
    return type(name, (C5b9, ), attrs)


def MBL_factory(proteins: dict[str]):
    C5b9 = proteins["C5b-9"]
    MBLs = {(name := f"C5b-9{'' if i == 1 else f'({i})'}"):
            new_MBL(name, i, C5b9) for i in range(1, 17)}
    C9 = proteins["C9"]
    C9.base += list(MBLs.keys())[:-1]
    C9.combination += list(MBLs.keys())[1:]
    return MBLs


from protein_towers.protein_information import get_data
from protein_towers.protein_full_bases import BasicTower, \
    CleavableTower, SelfActivatableTower, ActivatableTower
from protein_towers.protein_final_bases import injections, MBL_factory


def inject_base(name: str, attrs: dict[str]):
    if name in injections:
        return injections[name]
    if attrs["self_cleave"]:
        return CleavableTower
    if attrs["self_activate"]:
        return SelfActivatableTower
    if attrs["activatable"]:
        return ActivatableTower
    return BasicTower


def get_proteins(pull=True):
    protein_info = get_data(pull)
    proteins = {name: type(name, (inject_base(name, attrs),), attrs)
                for name, attrs in protein_info.items()}
    proteins |= MBL_factory(proteins)
    return proteins


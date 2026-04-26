import pandas as pd
from pandas._libs.parsers import STR_NA_VALUES  # noqa
from protein_towers.protein_information import clean_data

file = "enemies_data"
custom_na = STR_NA_VALUES - {"None"}


def pull_data():
    """Read spreadsheets in from Google sheets."""
    sheet_id = "1QVIrKeDk8QzO0-v1ayPLH2Vaj1Hc9gY5ZljJ9U2qiZc"
    url = "https://docs.google.com/spreadsheets/d/%s/gviz/tq?tqx=out:csv&sheet=%s"
    df = pd.read_csv(url % (sheet_id, "Sheet4"), keep_default_na=False, na_values=custom_na)
    defaults = pd.read_csv(url % (sheet_id, "Sheet5"))
    clean_data(df, defaults)
    df.to_csv(file, index=False)


def tuple_eval(key: str, x: (int | str)):
    if key not in ("info",) and ',' in str(x):
        items = []
        for i in (j.strip() for j in x.split(',')):
            if i and key in ("bases", "upper"):
                items.append(i)
            elif i:
                items.append(int(i) if i.isdigit() else i)
        return items
    return x


def get_data(pull=False) -> dict[str, dict[str]]:
    if pull:
        pull_data()
    df = pd.read_csv(file, keep_default_na=False)
    df.set_index("name", inplace=True)
    d = df.to_dict(orient="index")
    return {x: {w: tuple_eval(w, z) for w, z in y.items()} for x, y in d.items()}
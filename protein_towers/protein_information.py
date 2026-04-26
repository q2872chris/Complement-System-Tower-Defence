import pandas as pd
from pandas._libs.parsers import STR_NA_VALUES  # noqa

file = "proteins"
custom_na = STR_NA_VALUES - {"None"}

def clean_data(df, defaults):
    defaults = defaults.fillna("").to_dict(orient="list")
    defaults = {key: value[0] for key, value in defaults.items()}
    df.drop(df.columns[df.columns.str.contains("Unnamed")], axis=1, inplace=True)
    df.rename(columns=lambda x: str(x).strip().lower(), inplace=True)
    df.drop(df["name"][df["name"].isnull()].index, axis=0, inplace=True)
    df.fillna(defaults, inplace=True)
    df.dropna(how="all", axis=1, inplace=True)
    tuple_keys = [key for key, value in defaults.items() if ',' in str(value)]
    df[tuple_keys] = df[tuple_keys].apply(lambda x: x + ",")
    float_indices = df.columns[df.dtypes == "float64"]
    int_float_indices = [i for i in float_indices if df[i].apply(float.is_integer).all()]
    df[int_float_indices] = df[int_float_indices].astype(int)


def pull_data():
    """Read spreadsheets in from Google sheets."""
    sheet_id = "1QVIrKeDk8QzO0-v1ayPLH2Vaj1Hc9gY5ZljJ9U2qiZc"
    url = "https://docs.google.com/spreadsheets/d/%s/gviz/tq?tqx=out:csv&sheet=%s"
    df = pd.read_csv(url % (sheet_id, "Sheet1"), keep_default_na=False, na_values=custom_na)
    df_info = pd.read_csv(url % (sheet_id, "Sheet2")).fillna("")
    defaults = pd.read_csv(url % (sheet_id, "Sheet3"))
    clean_data(df, defaults)
    df["game_info"] = df["game_info"].apply(lambda x: x.replace('\n', ' '))
    df_info["info"] = df_info["info"].apply(lambda x: x.replace('\n', ' '))
    df = df.merge(df_info, on="name", how="left")
    df.to_csv(file, index=False)


def tuple_eval(key: str, x: (int | str)):
    if key not in ("info", "game_info") and ',' in str(x):
        items = []
        for i in (j.strip() for j in x.split(',')):
            if key in ("cleave", "move_cleave"):
                if ';' in i:
                    items.append([j.strip() for j in i[1:-1].split(';')])
                elif i:
                    items.append([i])
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




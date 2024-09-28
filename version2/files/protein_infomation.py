from ast import literal_eval
import pandas as pd
import re

is_tuple = re.compile("^.*?([a-zA-Z])?.*,")     # lazy quantifier used


def fill_nan(x):
    if type(x) != str:
        return 0
    if r := is_tuple.match(x):
        if r.group(1) is None:
            return "0,0,0"
    return ""


def pull_data():
    # read spreadsheets in from Google sheets
    sheet_id = "1QVIrKeDk8QzO0-v1ayPLH2Vaj1Hc9gY5ZljJ9U2qiZc"
    url = "https://docs.google.com/spreadsheets/d/%s/gviz/tq?tqx=out:csv&sheet=%s"
    df = pd.read_csv(url % (sheet_id, "Sheet1"))
    df_info = pd.read_csv(url % (sheet_id, "Sheet2"))
    # strip keys
    df.rename(columns=lambda x: str(x).strip(), inplace=True)
    # drop invalid rows and columns
    nameless_columns = [j for i, j in enumerate(df.keys()) if j == f"Unnamed: {i}"]
    empty_columns = [i for i in df.keys() if df[i].isnull().all()]
    nameless_rows = [i for i, j in enumerate(df["name"]) if type(j) == float]
    df.drop(nameless_columns + empty_columns, axis=1, inplace=True)
    df.drop(nameless_rows, inplace=True)
    # fill in nan values
    defaults = {i: fill_nan(df[i][df[i].notnull()].iloc[0]) for i in df}
    df.fillna(defaults, inplace=True)
    # change all columns with at least one tuple to all tuple
    for i in df:
        if any(is_tuple.match(str(j)) for j in df[i]) and i != "info":
            df[i] = [j + "," for j in df[i]]
    # change columns of float ints to ints
    float_indices = df.keys()[df.dtypes == "float64"]
    int_float_indices = [i for i in float_indices if df[i].apply(float.is_integer).all()]
    df[int_float_indices] = df[int_float_indices].astype(int)
    # add info column
    df["info"] = [str(i).replace("\n", " ") for i in df_info["info"].values]
    # save spreadsheet
    df.to_csv("files/proteins", index=False)


def tuple_eval(key, x):
    if key != "info" and (r := is_tuple.match(str(x).strip())):
        if r.group(1) is None and r.group(0) != ",":
            return literal_eval(x)
        return literal_eval(",".join(f"'{j.strip()}'" for j in x.split(",")))
    return x


def get_data(pull=False):
    if pull:
        pull_data()
    df = pd.read_csv("files/proteins", keep_default_na=False)
    df.set_index("name", inplace=True)
    d = df.to_dict(orient="index")
    return {x: {w: tuple_eval(w, z) for w, z in y.items()} for x, y in d.items()}


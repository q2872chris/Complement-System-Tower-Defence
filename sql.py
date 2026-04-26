import sqlite3
# At least one attribute in addition to ID is assumed for all tables

game_vars = {"gold": "int", "lives": "int", "wave": "int"}
tower_vars = {"type": "string", "x": "int", "y": "int",
              "upgrade1": "int", "upgrade2": "int", "upgrade3": "int",
              "upgrade4": "int"}
protein_vars = {"type": "string", "unlocked": "int", "number": "int"}
announcement_vars = {"announcement": "string"}


def fields_str(attrs: dict[str, str]) -> str:
    return ", \n\t\t".join(f"{key} {value} not null" for key, value in attrs.items())

def create_table(table: str, attrs: dict[str, str]) -> str:
    return f"""
    create table if not exists {table} (
        ID string not null,
        {fields_str(attrs)},
        foreign key (ID) references game (ID) on delete cascade
    )
"""

def save_str(table: str, attrs: dict[str, str]) -> str:
    return f"""
    insert into {table} (ID, {", ".join(attrs.keys())}) 
    values({"?, " * len(attrs)}?)
"""

def load_str(table: str, attrs: dict[str, str]) -> str:
    return f"""
    select {", ".join(attrs.keys())} from {table}
    where ID = '%s'
"""


game_sql_str = f"""
    create table if not exists game (
        ID string primary key,
        {fields_str(game_vars)}
    )
"""
towers_sql_str = create_table("towers", tower_vars)
proteins_sql_str = create_table("proteins", protein_vars)
announcements_sql_str = create_table("announcements", announcement_vars)

save_game_sql_str = save_str("game", game_vars)
save_towers_sql_str = save_str("towers", tower_vars)
save_proteins_sql_str = save_str("proteins", protein_vars)
save_announcements_sql_str = save_str("announcements", announcement_vars)

load_game_sql_str = load_str("game", game_vars)
load_towers_sql_str = load_str("towers", tower_vars)
load_proteins_sql_str = load_str("proteins", protein_vars)
load_announcements_sql_str = load_str("announcements", announcement_vars)


def sql_commit(con: sqlite3.Connection):
    con.commit()
    con.close()

def sql_setup() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    con = sqlite3.connect("saves.db")
    cur = con.cursor()
    cur.execute("pragma foreign_keys = on")
    cur.execute(game_sql_str)
    cur.execute(towers_sql_str)
    cur.execute(proteins_sql_str)
    cur.execute(announcements_sql_str)
    return con, cur

def save_game(name: str, game_info: list, proteins_info: list[tuple],
              towers_info: list[tuple], announcements: list[str]):
    con, cur = sql_setup()
    cur.execute(f"delete from game where ID = '{name}'")
    cur.execute(save_game_sql_str, [name, *game_info])
    for protein in proteins_info:
        cur.execute(save_proteins_sql_str, [name, *protein])
    for tower in towers_info:
        cur.execute(save_towers_sql_str, [name, *tower])
    for announcement in announcements:
        cur.execute(save_announcements_sql_str, [name, announcement])
    sql_commit(con)

def load_game(name: str) -> tuple:
    con, cur = sql_setup()
    cur.execute(load_game_sql_str % name)
    game_output = cur.fetchone()
    cur.execute(load_proteins_sql_str % name)
    proteins_output = cur.fetchall()
    cur.execute(load_towers_sql_str % name)
    towers_output = cur.fetchall()
    cur.execute(load_announcements_sql_str % name)
    announcements_output = cur.fetchall()
    sql_commit(con)
    return game_output, proteins_output, towers_output, announcements_output


if __name__ == "__main__":
    for var_name, var in globals().copy().items():
        if type(var) is str and "__" not in var_name:
            print(f"{var_name}:{var}")

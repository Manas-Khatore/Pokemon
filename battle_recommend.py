import pandas as pd
import psycopg2 as pg
import pk_types
from itertools import islice

conn = pg.connect(
    dbname="pokemon",  # Replace with your database name
    user="postgres",   # Replace with your username   # Replace with your password
    password="$manas"
)

cur = conn.cursor()
cur.execute("""SELECT * FROM pokemon_moves_full;""")
col_names = [desc[0] for desc in cur.description]
pokemon_moves_full = pd.DataFrame(cur.fetchall(), columns=col_names)

def move_recommend(pokemon_team):
    team_weaknesses = pk_types.team_categorize(pokemon_team)[0]
    top_weaknesses = dict(islice(team_weaknesses.items(), 3))
    final_weaknesses = {k: v for k, v in top_weaknesses.items() if len(v) > 0}
    move_recommend_df = pd.DataFrame()

    for pok_type in final_weaknesses:
        weak_pokemon = final_weaknesses[pok_type]
        move_recommend_df = pd.concat([move_recommend_df, strong_moves(pokemon_team, weak_pokemon, pok_type)])

    return move_recommend_df


def strong_moves(pokemon_team, weak_pokemon, pok_type):
    strong_moves_df = pd.DataFrame()
    remaining_pokemon = list(set(pokemon_team) - set(weak_pokemon))
    pok_type_weaknesses = list(pk_types.Weakness_Graph.successors(pok_type))
    attacking_moves_df = pokemon_moves_full[pokemon_moves_full["category"] != "Status"]
    for pok in remaining_pokemon:
        pok_moves_df = attacking_moves_df[attacking_moves_df["pokemon_name"] == pok]
        pok_strong_moves_df = pok_moves_df[pok_moves_df["type"].isin(pok_type_weaknesses)].reset_index()
        strong_moves_df = pd.concat([strong_moves_df, pok_strong_moves_df], ignore_index=True)
    
    weak_type_col = [pok_type for i in range(len(strong_moves_df))]
    strong_moves_df["weakness"] = weak_type_col
    strong_moves_df = strong_moves_df.rename(columns={"type": "move_type"})
    return strong_moves_df[["pokemon_name", "move_name", "move_type", "weakness"]].drop_duplicates().reset_index(drop=True)
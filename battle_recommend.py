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
pokemon_moves_full = pd.DataFrame(cur.fetchall())

def move_recommend(pokemon_team):
    team_weaknesses = pk_types.team_categorize(pokemon_team)[0]
    top_weaknesses = dict(islice(team_weaknesses.items(), 3))
    final_weaknesses = {k: v for k, v in top_weaknesses.items() if len(v) > 0}

    for pok_type in final_weaknesses:
        weak_pokemon = final_weaknesses[pok_type]

def strong_moves(pokemon_team, weak_pokemon, pok_type):
    remaining_pokemon = list(set(pokemon_team) - set(weak_pokemon))
    pok_type_weaknesses = pk_types.Weakness_Graph.successors(pok_type)
    for pok in pok_type_weaknesses:
        print(pok)

strong_moves([], [], "Grass")
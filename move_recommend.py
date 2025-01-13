import pandas as pd
import psycopg2 as pg
import pk_types

conn = pg.connect(
    dbname="pokemon",  # Replace with your database name
    user="postgres",   # Replace with your username   # Replace with your password
    password="$manas"
)

cur = conn.cursor()
cur.execute("""SELECT * FROM pokemon_moves_full;""")
pokemon_moves_full = pd.DataFrame(cur.fetchall())



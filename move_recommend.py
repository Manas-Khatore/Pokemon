import pandas as pd
import psycopg2 as pg

conn = pg.connect(
    dbname="pokemon",  # Replace with your database name
    user="postgres",         # Replace with your username   # Replace with your password
    password="$manas"
)


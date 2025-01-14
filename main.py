# cd into directory where project is stored
# run uvicorn main:app --reload in terminal to launch app

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
import matplotlib.pyplot as plt
import pandas as pd
import pk_types
import battle_recommend
import io
import os
from itertools import islice
from PIL import Image

app = FastAPI()

@app.get("/typegraph")
async def create_pokemon(pokemon: str):
    fig = pk_types.draw_type_relationship(pokemon)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    img = Image.open(buf)

    return Response(content=buf.getvalue(), media_type="image/png")

@app.get("/teamstats")
async def team_stats(pok1: str, 
                          pok2: str | None = None,
                          pok3: str | None = None,
                          pok4: str | None = None,
                          pok5: str | None = None,
                          pok6: str | None = None):
    
    dict_list = pk_types.team_categorize([pok1, pok2, pok3, pok4, pok5, pok6])
    weakness_dict, resist_dict, immune_dict = dict_list[0], dict_list[1], dict_list[2]
    top_weaknesses = dict(islice(weakness_dict.items(), 3))
    top_resistances = dict(islice(resist_dict.items(), 3))

    final_weaknesses = {k: v for k, v in top_weaknesses.items() if len(v) > 0}
    final_resistances = {k: v for k, v in top_resistances.items() if len(v) > 0}
    final_immunities = {k: v for k, v in immune_dict.items() if len(v) > 0}

    return {"Top 3 Weaknesses": final_weaknesses, 
            "Top 3 Resistances": final_resistances, 
            "All Immunities": final_immunities}

@app.get("/newmoves", response_class=HTMLResponse)
async def move_recommendations(pok1: str, 
                          pok2: str | None = None,
                          pok3: str | None = None,
                          pok4: str | None = None,
                          pok5: str | None = None,
                          pok6: str | None = None):
    
    pok_team = [pok1, pok2, pok3, pok4, pok5, pok6]
    pok_team = [pok for pok in pok_team if pok is not None]
    move_recommend_df = battle_recommend.move_recommend(pok_team)
    return move_recommend_df.to_html()
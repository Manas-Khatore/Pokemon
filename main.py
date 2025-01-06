from fastapi import FastAPI, Response
import matplotlib.pyplot as plt
import pk_types
import io
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

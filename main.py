from fastapi import FastAPI
import pk_types

app = FastAPI()

# print("hello")
# print(pk_types.type_categorize("Bulbasaur"))

@app.get("/")
async def create_pokemon(pokemon: str):
    return pk_types.type_categorize(pokemon)

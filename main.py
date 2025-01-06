from fastapi import FastAPI
import pk_types

app = FastAPI()

# print("hello")
# print(pk_types.type_categorize("Bulbasaur"))

@app.post("/items/")
async def create_item(pokemon: str):
    return pokemon

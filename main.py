from fastapi import FastAPI
import pk_types

app = FastAPI()

# print("hello")
# print(pk_types.type_categorize("Bulbasaur"))

@app.get("/")
async def root():
    return {"message": pk_types.type_categorize("Bulbasaur")}

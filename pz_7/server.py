from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cadet(BaseModel):
    id: int
    name: str

cadets_db = []

@app.post("/process-cadet")
async def process_cadet(cadet: Cadet):
    cadets_db.append(cadet)
    return {"status": "success", "cadet": cadet}

@app.get("/cadets")
async def get_cadets():
    return {"cadets": cadets_db}
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Cadet(BaseModel):
    id: int
    name: str
    rank: str


cadets_db: List[Cadet] = [
    Cadet(id=1, name="Иванов", rank="курсант"),
    Cadet(id=2, name="Петров", rank="сержант")
]


@app.get("/")
async def root():
    return {"message": "Добро пожаловать в систему курсантов"}

@app.get("/cadets", response_model=List[Cadet])
async def get_cadets():
    return cadets_db

@app.post("/cadets")
async def add_cadet(cadet: Cadet):
    cadets_db.append(cadet)
    return {"message": "Курсант добавлен"}

@app.delete("/cadets/{cadet_id}")
async def delete_cadet(cadet_id: int):
    global cadets_db
    cadets_db = [c for c in cadets_db if c.id != cadet_id]
    return {"message": "Курсант удален"}

@app.put("/cadets/{cadet_id}")
async def update_cadet(cadet_id: int, cadet: Cadet):
    for i, c in enumerate(cadets_db):
        if c.id == cadet_id:
            cadets_db[i] = cadet
            return {"message": "Данные курсанта обновлены"}
    return {"error": "Курсант не найден"}


app.mount("/static", StaticFiles(directory="static"), name="static")
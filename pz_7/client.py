from fastapi import FastAPI
import httpx
from pydantic import BaseModel

app = FastAPI()

class Cadet(BaseModel):
    id: int
    name: str

SERVER_URL = "http://localhost:8001"

@app.post("/send-cadet")
async def send_cadet(cadet: Cadet):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVER_URL}/process-cadet", json=cadet.dict())
        return response.json()
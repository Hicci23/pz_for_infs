from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cadets")
async def list_cadets(request: Request):
    cadets = [
        {"id": 1, "name": "Иванов", "rank": "курсант"},
        {"id": 2, "name": "Петров", "rank": "сержант"}
    ]
    return templates.TemplateResponse("cadets.html", {"request": request, "cadets": cadets})

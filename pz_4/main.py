from fastapi import FastAPI
from .controllers import cadet_controller

app = FastAPI()
app.include_router(cadet_controller.router)
from pydantic import BaseModel

class Cadet(BaseModel):
    id: int
    name: str
    rank: str
from fastapi import APIRouter, HTTPException
from ..models.cadet_model import Cadet
from ..services.cadet_service import CadetService

router = APIRouter()
service = CadetService()

@router.get("/cadets", response_model=list[Cadet])
async def get_cadets():
    return service.get_all()

@router.post("/cadets", response_model=Cadet)
async def create_cadet(cadet: Cadet):
    return service.add(cadet)

@router.put("/cadets/{cadet_id}")
async def update_cadet(cadet_id: int, cadet: Cadet):
    if not service.update(cadet_id, cadet):
        raise HTTPException(status_code=404, detail="Курсант не найден")
    return {"message": "Данные курсанта обновлены"}

@router.delete("/cadets/{cadet_id}")
async def delete_cadet(cadet_id: int):
    if not service.delete(cadet_id):
        raise HTTPException(status_code=404, detail="Курсант не найден")
    return {"message": "Курсант удален"}

from fastapi import APIRouter
from app.models.requests import FarmListRequest
from app.service.BotService import bot_service

router = APIRouter(prefix="/api/farm", tags=["Farm"])


@router.post("/send")
def send_farmlist(data: FarmListRequest):
    bot_service.send_farmlist(data.list)
    return {"status": "success", "message": "Farm list sent"}

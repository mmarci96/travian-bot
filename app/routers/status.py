from fastapi import APIRouter
from app.service.BotService import bot_service

router = APIRouter(prefix="/status", tags=["Status"])


@router.get("/")
def status():
    return bot_service.get_status()

from fastapi import APIRouter
from app.models.requests import LoginRequest
from app.service.BotService import bot_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data: LoginRequest):
    return bot_service.init_bot(data.url, data.username, data.password)

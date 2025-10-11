from fastapi import APIRouter
from app.models.requests import ResourceTaskRequest
from app.service.BotService import bot_service

router = APIRouter(prefix="/api/villages", tags=["Villages"])


@router.get("/")
def villages():
    return {"status": "success", "data": bot_service.get_villages()}


@router.post("/tasks")
def add_task_to_village(data: ResourceTaskRequest):
    res = bot_service.add_resource_task(
        data.village_id, data.resource_type, data.target_level
    )
    return {"status": "success", "message": res}


@router.get("/constructions")
def get_constructions():
    data = bot_service.get_constructions()
    if data is None:
        return {
            "status": "error",
            "message": "No constructions found",
        }
    return {"status": "success", "data": data}


@router.get("/{village_id}/constructions")
def get_constructions_by_village_id(village_id: str):
    data = bot_service.get_constructions_by_village_id(village_id)
    if data is None:
        return {
            "status": "error",
            "message": f"No village with id {village_id}",
        }
    return {"status": "success", "data": data}

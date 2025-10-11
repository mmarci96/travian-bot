from pydantic import BaseModel
from typing import List


class LoginRequest(BaseModel):
    url: str
    username: str
    password: str


class BuildingRequest(BaseModel):
    village_id: str
    slot_id: str
    building_id: str


class ResourceTaskRequest(BaseModel):
    village_id: str
    resource_type: str
    target_level: int


class FarmListRequest(BaseModel):
    list: List[int]

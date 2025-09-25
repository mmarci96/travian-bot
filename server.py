from time import sleep
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from threading import Lock, Thread
from contextlib import asynccontextmanager
import time

from app.Bot import Bot

# Singleton bot and lock
bot: Optional[Bot] = None
bot_lock = Lock()


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


def loop_check_queue():
    """Background thread to check build queue every 10 sec"""
    global bot
    while True:
        with bot_lock:
            if bot:
                try:
                    bot.get_build_queue()
                except Exception as e:
                    print(f"[!] Error in build queue loop: {e}")
        time.sleep(10)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    t = Thread(target=loop_check_queue, daemon=True)
    t.start()
    print("[✓] Background build queue thread started.", app.title)
    yield
    # Shutdown
    print("[✗] Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.get("/status")
def status():
    with bot_lock:
        if not bot:
            return {"status": "error", "message": "Bot not initialized"}
        if hasattr(bot, "get_status"):
            return {"status": "success", "message": bot.get_status()}
        return {"status": "success", "message": "Bot running"}


@app.post("/login")
def login(data: LoginRequest):
    print("[✓] Login request received.")
    global bot
    with bot_lock:
        if bot:
            return {"status": "success", "message": "Already logged in"}

        bot = Bot(data.url, data.username, data.password)
        bot.login()
        sleep(2)
        if bot.is_logged():
            bot.setup()
            return {"status": "success", "message": "Logged in"}
        else:
            bot = None  # reset if login failed
            return {"status": "error", "message": "Login failed"}


@app.post("/update")
def update():
    with bot_lock:
        if not bot:
            return {"status": "error", "message": "Bot not initialized"}
        bot.update()
    return {"status": "success", "message": "Villages updated"}


@app.post("/test_build")
def test_build():
    with bot_lock:
        if not bot:
            return {"status": "error", "message": "Bot not initialized"}
        bot.test_build()
    return {"status": "success", "message": "Build task triggered"}


@app.post("/send_farmlist")
def send_farmlist(data: FarmListRequest):
    with bot_lock:
        if not bot:
            return {"status": "error", "message": "Bot not initialized"}
        bot.send_list(data.list)
    return {"status": "success", "message": "Farm list sent"}


@app.get("/villages")
def villages():
    if not bot:
        return {"status": "error", "message": "Bot not initialized"}
    data = bot.get_villages()
    return {"status": "success", "data": data}


@app.post("/villages/tasks")
def add_task_to_village(data: ResourceTaskRequest):
    if not bot:
        return {"status": "error", "message": "Bot not initialized"}
    res = bot.build_resource(
        data.village_id, data.resource_type, data.target_level
    )
    return {"status": "success", "message": res}


@app.get("/villages/{village_id}/constructions")
def get_constructions_by_village_id(village_id: str):
    if not bot:
        return {"status": "error", "message": "Bot not initialized"}

    data = bot.get_constructions_by_village_id(village_id)
    if data is None:
        return {
            "status": "error",
            "message": f"No village with id {village_id}",
        }

    return {"status": "success", "data": data}

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.Logger import msg
from app.TaskManager import start_background_tasks, start_bot
from app.routers import auth, status, villages, farm
from dotenv import load_dotenv
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    url = os.getenv("URL", "url")
    username = os.getenv("USERNAME", "username")
    password = os.getenv("PASSWORD", "password")

    start_bot(url, username, password)  # runs Selenium bot in background
    start_background_tasks()  # runs loop_check_queue thread

    yield
    msg(f"[✗] Shutting down app: {app.title} ...")


app = FastAPI(
    lifespan=lifespan,
    title="Travian Bot API",
    description="Bot automation and management API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Register routers
app.include_router(auth.router)
app.include_router(status.router)
app.include_router(villages.router)
app.include_router(farm.router)

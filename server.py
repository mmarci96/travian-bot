import sys
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.TaskManager import start_background_tasks
from app.routers import auth, status, villages, farm
from enum import Enum
from datetime import datetime


class LogType(Enum):
    ERROR = "[ERROR]"
    WARN = "[WARN]"
    INFO = "[INFO]"
    RUN = "[RUN]"


def msg(msg: str, log_type=LogType.INFO):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f" [{timestamp}] {log_type.value} {msg}")
    sys.stdout.flush()


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_background_tasks()
    yield
    msg(f"[✗] Shutting down app:{app.title} ...")


app = FastAPI(lifespan=lifespan)

# Register routers
app.include_router(auth.router)
app.include_router(status.router)
app.include_router(villages.router)
app.include_router(farm.router)

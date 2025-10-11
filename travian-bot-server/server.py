from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.Logger import msg
from app.TaskManager import start_background_tasks
from app.routers import auth, status, villages, farm


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_background_tasks()
    yield
    msg(f"[✗] Shutting down app:{app.title} ...")


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

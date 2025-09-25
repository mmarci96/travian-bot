from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.TaskManager import start_background_tasks
from app.routers import auth, status, villages, farm


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_background_tasks()
    yield
    print("[✗] Shutting down...", app.title)


app = FastAPI(lifespan=lifespan)

# Register routers
app.include_router(auth.router)
app.include_router(status.router)
app.include_router(villages.router)
app.include_router(farm.router)

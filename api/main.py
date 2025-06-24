from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.postgres import database
from routers.analytics import router as analytics_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(analytics_router)
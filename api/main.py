"""
main.py

FastAPI application entry point for the enterprise analytics API platform.
Configures database connections, routers, and application lifecycle management.

The application uses asynchronous programming with FastAPI and async database 
connections to handle high-concurrency workloads efficiently, enabling the platform 
to serve concurrent analytics requests without blocking operations.
"""

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
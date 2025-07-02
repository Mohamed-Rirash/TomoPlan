from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.logs import logger
from src.auth.router import router as auth_router
from src.config import settings
from src.database import session
from src.initdb import init
from src.midlewares import LoguruExceptionMiddleware
from src.tasks.router import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize tables
    try:
        await init()
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        raise

    # Connect to database
    try:
        await session.connect()
        print("Database connected successfully")
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        raise

    try:
        yield
    finally:
        # Disconnect from database
        try:
            await session.disconnect()
            print("Database disconnected successfully")
        except Exception as e:
            print(f"Error disconnecting from database: {e}")


DESCRIPTION = """
    TomoPlan is an AI-powered task management application that helps you 
    prioritize your daily tasks by asking you 3 things to do 
    tomorrow at bedtime, and then organizes and prioritizes your
    progress and stay on track. With TomoPlan, you can avoid wasting your
    time on unimportant tasks and focus on what really matters.
"""
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_V1_STR,
    description=DESCRIPTION,
    lifespan=lifespan,
)

# ✅ Add the middleware
app.add_middleware(LoguruExceptionMiddleware)

# ✅ Optional: configure Loguru
logger.add(
    "logs/error.log", level="ERROR", rotation="500 KB", retention="7 days", enqueue=True
)


def get_cors_origins() -> List[str]:
    if isinstance(settings.BACKEND_CORS_ORIGINS, str):
        return [origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",")]
    return [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to TomoPlan!"}


app.include_router(tasks_router)
app.include_router(auth_router)

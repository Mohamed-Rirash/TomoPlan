from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from limits.storage import RedisStorage
from loguru import logger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.agent.router import router as agent_router
from src.auth.router import router as auth_router
from src.config import settings
from src.database import session
from src.initdb import init
from src.midlewares import LoguruExceptionMiddleware, RateLimitMiddleware
from src.notifications.router import router as notif_router
from src.notifications.scheduler import schedule_reminders
from src.tasks.router import router as tasks_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await schedule_reminders()
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
TomoPlan is an AI-powered task management application designed to help you optimize your daily productivity.

Key Features:
- 📝 Task Management: Create, update, and delete tasks with priority levels (LOW, MEDIUM, HIGH, CRITICAL)
- 🤖 AI Assistant: AI-powered task planning and optimization
- 📱 Real-time Notifications: Stay updated with task reminders and progress
- 🔄 Task Planning: Plan your daily tasks using AI recommendations
- 🔐 Secure Authentication: Protected API endpoints with JWT authentication

The API is organized into several key components:

1. Authentication (`/auth`)
   - User registration and login
   - Password management
   - Profile updates

2. Tasks (`/tasks`)
   - CRUD operations for tasks
   - Task prioritization
   - Task filtering and pagination
   - Task status updates

3. AI Agent (`/agent`)
   - AI-powered task planning
   - Task breakdown and optimization
   - Daily task recommendations

4. Notifications (`/notifications`)
   - Real-time notification streaming
   - Task reminder system
   - Progress updates

Security:
- All endpoints require JWT authentication (except auth endpoints)
- CORS enabled for frontend communication
- Secure password hashing

Environment:
- Local development: http://localhost:8000
- Production: Configurable via environment variables

For more information about specific endpoints, use the interactive API documentation available at `/docs` and `/redoc`
"""

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_V1_STR,
    description=DESCRIPTION,
    lifespan=lifespan,
    contact={
        "name": "TomoPlan Support",
        "url": "https://github.com/Mohamed-Rirash/TomoPlan",
        "email": "support@tomoplan.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)
app.add_middleware(RateLimitMiddleware, rate="5/minute")
# ✅ Add the middleware
# app.add_middleware(LoguruExceptionMiddleware)

# ✅ Optional: configure Loguru
# logger.add(
# "logs/error.log", level="ERROR", rotation="500 KB", retention="7 days", enqueue=True
# )


def get_cors_origins() -> list[str]:
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


app.include_router(auth_router, prefix=f"{settings.API_V1_STR}")
app.include_router(tasks_router, prefix=f"{settings.API_V1_STR}")
app.include_router(notif_router, prefix=f"{settings.API_V1_STR}")
app.include_router(agent_router, prefix=f"{settings.API_V1_STR}")

# if you are using alembic no need for this
from src.database import engine, metadata, session
from src.tasks import models


async def init():
    try:
        # Create tables
        metadata.create_all(engine)
        print("Database tables are created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise

from databases import Database
from sqlalchemy import MetaData, create_engine

from src.config import settings

SQLALCHEMY_DATABASE_URI = str(settings.SQLALCHEMY_DATABASE_URI)

# Create engine with timezone support
engine = create_engine(
    SQLALCHEMY_DATABASE_URI.replace("+asyncpg", ""),
    pool_pre_ping=True,
    pool_recycle=300,
)

metadata = MetaData()

# Create database session with proper configuration
session = Database(
    SQLALCHEMY_DATABASE_URI,
    force_rollback=False,
)


# INFO: sqlite database connection

# from sqlalchemy import create_engine, MetaData


# from databases import Database

# metadata = MetaData()
# SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"

# engine = create_engine(SQLALCHEMY_DATABASE_URI)

# session = Database(SQLALCHEMY_DATABASE_URI)

from databases import Database
from sqlalchemy import MetaData, create_engine

from src.config import settings

SQLALCHEMY_DATABASE_URI = str(settings.SQLALCHEMY_DATABASE_URI)

engine = create_engine(SQLALCHEMY_DATABASE_URI.replace("+asyncpg", ""))
# SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URI)
metadata = MetaData()

session = Database(SQLALCHEMY_DATABASE_URI)

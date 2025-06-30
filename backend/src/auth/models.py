import uuid

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table, Uuid, func

from src.database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Uuid, primary_key=True, default=uuid.uuid4),
    Column("first_name", String(100), nullable=False),
    Column("last_name", String(100), nullable=False),
    Column("email", String(100), nullable=False),
    Column("password", String, nullable=False),
    Column("is_active", Boolean, nullable=False, default=False),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime),
)

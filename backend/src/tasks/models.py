# src/tasks/models.py
import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Index,
    String,
    Table,
    Text,
    Uuid,
    func,
)

from src.database import metadata


class TaskPriority(str, PyEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


task_table = Table(
    "tasks",
    metadata,
    Column("id", Uuid, primary_key=True, default=uuid.uuid4),
    Column("name", String(100), nullable=False),
    Column("description", Text, nullable=False),
    Column("due_date", DateTime(timezone=True), nullable=True),
    Column("priority", Enum(TaskPriority), nullable=False, default=TaskPriority.LOW),
    Column("is_done", Boolean, nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
)

Index("idx_task_name", task_table.c.name)

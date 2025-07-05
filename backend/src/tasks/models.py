# src/tasks/models.py
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    Table,
    Text,
    Uuid,
    func,
)

from src.database import metadata
from src.tasks.utils import TaskPriority

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
    Column("user_id", Uuid, ForeignKey("users.id"), nullable=False),
)

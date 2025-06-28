import uuid
from enum import Enum as PyEnum

from sqlalchemy import UUID, Boolean, Column, DateTime, Index, String, Table, Text, Enum

from src.database import metadata


class TaskPriority(PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

task_table = Table(
    "tasks",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid5(uuid.NAMESPACE_DNS, "task"),
    ),
    Column("name", String(100), nullable=False),
    Column("description", Text, nullable=False),
    Column("due_date", DateTime, nullable=False),
    Column(
        "priority",
        Enum(TaskPriority),
        nullable=False,
    ),
    Column("is_done", Boolean, nullable=False),
)
index = Index("idx_task_id", task_table.c.id)




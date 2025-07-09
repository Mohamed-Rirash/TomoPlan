# src/tasks/models.py
import uuid
from sqlalchemy import (
    Boolean,
    Column,
    Date,
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
from src.utils import TaskPriority

task_table = Table(
    "tasks",
    metadata,
    Column("id", Uuid, primary_key=True, default=uuid.uuid4),
    Column("name", String(100), nullable=False),
    Column("description", Text, nullable=False),
    Column("due_date", DateTime(timezone=True), nullable=True),
    Column("priority", Enum(TaskPriority), nullable=False, default=TaskPriority.LOW),
    Column("is_done", Boolean, nullable=False),
    Column("created_at", Date, default=func.now(), nullable=False, index=True),
    Column("user_id", Uuid, ForeignKey("users.id"), nullable=False),
)

Index("tasks_created_at_idx", task_table.c.created_at)
Index("tasks_user_id_idx", task_table.c.user_id)
Index("taskidx", task_table.c.id)

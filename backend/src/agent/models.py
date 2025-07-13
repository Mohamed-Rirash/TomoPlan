import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Time,
    Uuid,
    func,
)

from src.agent.schemas import TodoStatus
from src.database import metadata
from src.utils import TaskPriority

agent_task = Table(
    "agent_task",
    metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("task_name", String(100), nullable=False),
    Column("task_description", String, nullable=False),
    Column("task_priority", Enum(TaskPriority), nullable=False),
    Column("task_stimation", Time, nullable=False),
    Column(
        "tip",
        String,
    ),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
    Column("user_id", Uuid, ForeignKey("users.id"), nullable=False),
)


task_todo = Table(
    "task_todo",
    metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("task_num", Integer, nullable=False),
    Column("todo_name", String(100), nullable=False),
    Column("status", Enum(TodoStatus), nullable=False),
    Column("stimated_time", Time, nullable=False),
    Column("depends_on", String, nullable=True),
    Column("task_id", Uuid(as_uuid=True), ForeignKey("agent_task.id"), nullable=False),
)

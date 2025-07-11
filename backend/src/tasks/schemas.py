from datetime import date, datetime, timezone
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.tasks.models import TaskPriority


class TaskBase(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=1000)


class TaskCreate(TaskBase):
    is_done: bool = Field(False, description="Whether the task is done or not")
    due_date: Optional[datetime] = None
    priority: TaskPriority = Field(
        TaskPriority.LOW, description="The priority of the task"
    )

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
    priority: Optional[TaskPriority] = None


class Task(TaskBase):
    id: UUID
    is_done: bool
    due_date: Optional[datetime] = None
    created_at: date
    priority: TaskPriority
    user_id: UUID

from datetime import datetime, time
from enum import Enum
from typing import List, Optional
from uuid import UUID

from databases import Database
from pydantic import BaseModel, Field

from src.utils import TaskPriority


class TodoStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Todo(BaseModel):
    Task_num: int = Field(..., description="Task number based on which goes first")
    todo_name: str
    status: TodoStatus = TodoStatus.IN_PROGRESS
    stimated_time: time  # Consider changing to int (minutes)
    depends_on: Optional[List[int]] = Field(
        None, description="list of other breakdown IDs that this todo depends on"
    )


class Taskoutput(BaseModel):
    task_name: str
    task_description: str
    task_priority: TaskPriority
    task_stimation: str  # Consider changing to int (minutes)
    task_breakdown: List[Todo]
    tip: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class TaskInput(BaseModel):
    task_name: str
    task_description: str


class AgentDeps(BaseModel):
    db: Database

    class Config:
        arbitrary_types_allowed = True

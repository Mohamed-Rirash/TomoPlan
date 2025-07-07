from typing import List, Optional
from databases import Database
from pydantic import BaseModel
from datetime import datetime, time
from enum import Enum
from uuid import UUID


class TodoStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class TaskPriority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Todo(BaseModel):
    id: int
    todo_name: str
    status: TodoStatus = TodoStatus.PENDING
    stimated_time: str  # Consider changing to int (minutes)
    depends_on: Optional[List[int]] = None


class Taskoutput(BaseModel):
    id: UUID
    task_name: str
    task_description: str
    task_priority: TaskPriority
    task_stimation: str  # Consider changing to int (minutes)
    task_breakdown: List[Todo]
    tags: List[str] = []
    scheduled_start_time: Optional[time] = None
    scheduled_end_time: Optional[time] = None
    depends_on: List[int] = []
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    version: int = 1


class TaskInput(BaseModel):
    id: str
    task_name: str
    task_description: str


class AgentDeps(BaseModel):
    user_id: UUID
    db: Database

    class Config:
        arbitrary_types_allowed = True

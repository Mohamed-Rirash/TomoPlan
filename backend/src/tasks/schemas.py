from datetime import datetime
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str
    due_date: datetime
    # priority: TaskPriority
    is_done: bool

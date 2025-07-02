from uuid import UUID

from databases import Database
from fastapi import APIRouter, Depends, status

from src.dependency import get_db
from src.tasks.schemas import Task, TaskCreate, TaskUpdate
from src.tasks.services import (
    create_task,
    delete_task,
    read_all_tasks,
    read_task_by_id,
    update_task,
)
from src.dependency import user_dependecy

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


# get all task
@router.get("/", response_model=list[Task])
async def get_tasks(
    user: user_dependecy, limit: int = 10, page: int = 1, db: Database = Depends(get_db)
):
    return await read_all_tasks(limit, page, db)


# get task by id
@router.get("/{id}", response_model=Task)
async def get_task(id: UUID, db: Database = Depends(get_db)):
    return await read_task_by_id(id, db)


# post atask
@router.post("/", response_model=Task)
async def add_task(task: TaskCreate, db: Database = Depends(get_db)):
    return await create_task(task, db)


# update task
@router.put("/{id}")
async def Edit_task(id: UUID, task: TaskUpdate, db: Database = Depends(get_db)):
    return await update_task(id, task, db)


# delete task
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def Remove_task(id: UUID, db: Database = Depends(get_db)):
    return await delete_task(id, db)

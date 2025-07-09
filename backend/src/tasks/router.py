from typing import List, Union
from uuid import UUID

from databases import Database
from fastapi import APIRouter, Depends, HTTPException, status

from src.dependency import get_db
from src.tasks.schemas import Task, TaskCreate, TaskUpdate
from src.tasks.services import (
    delete_task,
    read_all_tasks,
    read_task_by_id,
    update_task,
    create_tasks,
)


from src.dependency import user_dependecy, db_dependency

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


# get all task
@router.get("/tasks", response_model=list[Task])
async def get_tasks(
    user: user_dependecy, limit: int = 10, page: int = 1, db: Database = Depends(get_db)
):
    user_id = user.id  # type: ignore
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await read_all_tasks(limit, page, db, user_id)


# get task by id
@router.get("/task/{id}", response_model=Union[Task, dict])
async def get_task(id: UUID, user: user_dependecy, db: Database = Depends(get_db)):
    user_id = user.id  # type: ignore
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = await read_task_by_id(id, db, user_id)
    if not result:
        return {"message": "Task not found"}

    return result


@router.post(
    "/addtask", response_model=Union[Task, List[Task]], status_code=status.HTTP_201_CREATED
)
async def add_task_or_tasks(
    body: Union[TaskCreate, List[TaskCreate]],
    user: user_dependecy,
    db: db_dependency,  # type: ignore
):
    user_id = user.id  # type: ignore
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # If body is a single task
    if isinstance(body, TaskCreate):
        return await create_tasks(body, db, user_id)  # type: ignore

    # If it's a list of tasks
    if isinstance(body, list):
        return await create_tasks(body, db, user_id)

    # fallback safety
    raise HTTPException(status_code=400, detail="Invalid input format")


# update task
@router.put("/task/{id}")
async def Edit_task(
    id: UUID, user: user_dependecy, task: TaskUpdate, db: Database = Depends(get_db)
):
    user_id = user.id  # type: ignore
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await update_task(id, task, db, user_id)


# delete task
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def Remove_task(id: UUID, db: db_dependency, user: user_dependecy):  # type: ignore
    user_id = user.id  # type: ignore
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await delete_task(id, db, user_id)

from databases import Database
from fastapi import APIRouter, Depends

from src.dependency import get_db
from src.tasks.schemas import Task, TaskCreate, TaskUpdate
from src.tasks.services import create_task, read_all_tasks

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


# get all task
@router.get("/", response_model=list[Task])
async def get_tasks(limit: int = 10, page: int = 1, db: Database = Depends(get_db)):
    return await read_all_tasks(limit, page, db)


# get task by id
@router.get("/{id}", response_model=Task)
async def get_task(id: str, db: Database = Depends(get_db)):
    pass


# post atask
@router.post("/", response_model=Task)
async def add_task(task: TaskCreate, db: Database = Depends(get_db)):
    return await create_task(task, db)


# update task
@router.put("/{id}", response_model=Task)
async def update_task(id: str, task: TaskUpdate):
    pass


# delete task
@router.delete("/{id}")
async def delete_task(id: str):
    pass

# src/tasks/services.py
import uuid
from datetime import timezone

from sqlalchemy import select
from .models import task_table


async def read_all_tasks(limit: int, page: int, db) -> list[dict]:
    offset = (page - 1) * limit
    query = select(task_table).offset(offset).limit(limit)
    results = await db.fetch_all(query)

    tasks = []
    for row in results:
        row_dict = dict(row._mapping)
        row_dict["id"] = str(row_dict["id"])
        tasks.append(row_dict)
    return tasks


async def read_task_by_id(id: uuid.UUID, db) -> dict | None:
    query = select(task_table).where(task_table.c.id == id)
    result = await db.fetch_one(query)

    if result:
        task_dict = dict(result._mapping)
        task_dict["id"] = str(task_dict["id"])
        return task_dict
    return None


async def create_task(data, db):
    task_id = uuid.uuid4()
    task_data = data.dict()

    # Ensure due_date is UTC if present
    due_date = task_data.get("due_date")
    if due_date and due_date.tzinfo is None:
        task_data["due_date"] = due_date.replace(tzinfo=timezone.utc)

    query = task_table.insert().values(id=task_id, **task_data)
    await db.execute(query)

    # Fetch the inserted row
    query = select(task_table).where(task_table.c.id == task_id)
    result = await db.fetch_one(query)
    task_dict = dict(result._mapping)
    task_dict["id"] = str(task_dict["id"])
    return task_dict


async def update_task(id: uuid.UUID, data, db):
    task = await read_task_by_id(id, db)
    if not task:
        return None
    query = task_table.update().where(task_table.c.id == id).values(**data.dict())
    await db.execute(query)
    return {"message": "Task updated successfully"}


async def delete_task(id: uuid.UUID, db):
    query = task_table.delete().where(task_table.c.id == id)
    await db.execute(query)

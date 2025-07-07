# src/tasks/services.py
import uuid
from datetime import timezone
from typing import Sequence, Union

from sqlalchemy import select

from .models import task_table
from .schemas import TaskCreate


async def read_all_tasks(limit: int, page: int, db, user_id) -> list[dict]:
    offset = (page - 1) * limit
    query = (
        select(task_table)
        .where(task_table.c.user_id == user_id)
        .order_by(task_table.c.id.desc())
        .limit(limit)
        .offset(offset)
    )
    results = await db.fetch_all(query)

    tasks = []
    for row in results:
        row_dict = dict(row._mapping)
        row_dict["id"] = str(row_dict["id"])
        tasks.append(row_dict)
    return tasks


async def read_task_by_id(id: uuid.UUID, db, user_id) -> dict | None:
    query = select(task_table).where(
        task_table.c.id == id and task_table.c.user_id == user_id
    )
    result = await db.fetch_one(query)

    if result:
        task_dict = dict(result._mapping)
        task_dict["id"] = str(task_dict["id"])
        return task_dict
    return None


async def create_tasks(data: Union[TaskCreate, Sequence[TaskCreate]], db, user_id):
    task_values = []

    # Handle single task case
    if isinstance(data, TaskCreate):
        data_list = [data]
    else:
        data_list = data

    # Prepare all task dicts with unique UUIDs
    for task_data in data_list:
        task_id = uuid.uuid4()
        task_dict = task_data.model_dump()

        # Ensure UTC-aware due_date
        due_date = task_dict.get("due_date")
        if due_date and due_date.tzinfo is None:
            task_dict["due_date"] = due_date.replace(tzinfo=timezone.utc)

        # Convert UUID to string for SQLite compatibility
        task_dict["id"] = task_id
        task_dict["user_id"] = str(user_id)
        task_values.append(task_dict)

    # Bulk insert with one DB call
    insert_query = task_table.insert()
    async with db.transaction():
        await db.execute_many(query=insert_query, values=task_values)

        # Now fetch inserted tasks by their UUIDs
        task_ids = [task["id"] for task in task_values]

        select_query = select(task_table).where(task_table.c.id.in_(task_ids))
        inserted_rows = await db.fetch_all(select_query)

    # Return serialized list
    return [dict(row._mapping) for row in inserted_rows]


# async def create_task(data, db, user_id):
#     task_id = uuid.uuid4()
#     task_data = data.dict()
#
#     # Ensure due_date is UTC if present
#     due_date = task_data.get("due_date")
#     if due_date and due_date.tzinfo is None:
#         task_data["due_date"] = due_date.replace(tzinfo=timezone.utc)
#
#     query = task_table.insert().values(user_id=user_id, id=task_id, **task_data)
#     result = await db.fetch_one(query)
#
#     # Fetch the inserted row
#     query = select(task_table).where(
#         task_table.c.id == task_id and task_table.c.user_id == user_id
#     )
#     result = await db.fetch_one(query)
#     task_dict = dict(result._mapping)
#     task_dict["id"] = str(task_dict["id"])


async def update_task(id: uuid.UUID, data, db, user_id):
    task = await read_task_by_id(id, db, user_id)
    if not task:
        return None
    query = (
        task_table.update()
        .where(task_table.c.id == id and task_table.c.user_id == user_id)
        .values(**data.dict())
    )
    await db.execute(query)
    return {"message": "Task updated successfully"}


async def delete_task(id: uuid.UUID, db, user_id):
    query = task_table.delete().where(
        task_table.c.id == id and task_table.c.user_id == user_id
    )
    await db.execute(query)

from datetime import date, timedelta, timedelta
from typing import Union
from uuid import UUID, uuid4
from sqlalchemy import select
from src.tasks.models import task_table

today = date.today()
day_back = timedelta(days=1)
yesterday = today - day_back


# fetch tasks from the database by date
async def get_todays_tasks(user_id: UUID, db):
    query = select(
        task_table.c.id,
        task_table.c.name,
        task_table.c.description,
        task_table.c.created_at,
    ).where(task_table.c.user_id == user_id and task_table.c.date == today)
    results = await db.fetch_all(query)
    if results:
        tasks = []
        for row in results:
            row_dict = dict(row._mapping)
            tasks.append(row_dict)
        return tasks
    return None

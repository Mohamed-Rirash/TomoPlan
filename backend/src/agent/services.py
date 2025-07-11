import uuid
from datetime import date, time, timedelta
from uuid import UUID

from sqlalchemy import select

from src.agent.models import agent_task, task_todo
from src.agent.schemas import Taskoutput  # Pydantic model
from src.database import Database  # adjust as needed
from src.tasks.models import task_table

today = date.today()
day_back = timedelta(days=1)
yesterday = today - day_back


# fetch tasks from the database by date
async def get_todays_tasks(user_id: UUID, db) -> list | None:
    query = select(
        task_table.c.id,
        task_table.c.name,
        task_table.c.description,
        task_table.c.created_at,
    ).where(task_table.c.user_id == user_id, task_table.c.created_at == today)
    results = await db.fetch_all(query)
    if results:
        tasks = []
        for row in results:
            row_dict = dict(row._mapping)
            tasks.append(row_dict)
        return tasks
    return None


async def store_planned_tasks(data: list[Taskoutput] | None, db: Database) -> str:
    if not data:
        return "⚠️ No tasks to store."

    task_rows = []
    breakdown_rows = []

    for task in data:
        task_id = uuid.uuid4()

        # ✅ Fix: access task_stimation correctly
        h, m = map(int, task.task_stimation.split(":"))
        stimation_time = time(hour=h, minute=m)

        task_rows.append(
            {
                "id": task_id,
                "task_name": task.task_name,
                "task_description": task.task_description,
                "task_priority": task.task_priority,
                "task_stimation": stimation_time,
                "tip": task.tip,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
            }
        )

        for subtask in task.task_breakdown:
            # ✅ Fix: stimated_time is already a time object (not a string)
            depends = subtask.depends_on
            depends_str = ",".join(str(d) for d in depends) if depends else None
            id = uuid.uuid4()

            breakdown_rows.append(
                {
                    "id": id,
                    "task_id": task_id,
                    "task_num": subtask.Task_num,
                    "todo_name": subtask.todo_name,
                    "status": subtask.status,
                    "stimated_time": subtask.stimated_time,
                    "depends_on": depends_str,
                }
            )

    # ✅ Store both in one transaction
    async with db.transaction():
        await db.execute_many(agent_task.insert(), task_rows)
        await db.execute_many(task_todo.insert(), breakdown_rows)

    return f"✅ Stored {len(task_rows)} tasks and {len(breakdown_rows)} subtasks."

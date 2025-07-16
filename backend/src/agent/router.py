from fastapi import APIRouter, HTTPException, status

from src.agent.ai_agent import plannner_agent, roast_agent
from src.agent.schemas import AgentDeps
from src.agent.services import get_users_tasks, store_planned_tasks
from src.auth.models import users
from src.dependency import db_dependency, user_dependecy

# from src.agent.models import task_breakdown_table, task_tags_table, agent_task

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
)


# @router.get("/todoes")
# async def read_from_agent(db: db_dependency):
#     deps = AgentDeps(db=db)
#
#     result = await plannner_agent.run(
#         "based on my task in that tool iwant to plan my day tasks Fetch today’s tasks, plan them step by step, and then store them in the database using `store_tasks`note if theres no task from the tool to get it i want you to return none .",
#         deps=deps,  # ✅ pass full deps here!
#     )
#     await store_planned_tasks(result.output, db)
#
#     return result.output


@router.get("/todoes")
async def read_from_agent(db: db_dependency):
    deps = AgentDeps(db=db)

    # 1. Run the planner
    plan_result = await plannner_agent.run(
        "Fetch today’s tasks and plan them step-by-step.",
        deps=deps,
    )
    tasks = plan_result.output  # list[Taskoutput]

    if tasks:
        await store_planned_tasks(tasks, db)
        return tasks

    # 2. Planner returned []  → ask roast_agent
    roast = await roast_agent.run("[]")
    return roast.output  # 🔥 the roast string


@router.post("/get-tasks")
async def get_todays_tasks(user: user_dependecy, db: db_dependency):
    user_id = users.id  # pyright: ignore[reportAttributeAccessIssue]
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="please login first"
        )
    return get_users_tasks(user_id, db)

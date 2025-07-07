# from databases import Database
# from fastapi import HTTPException, status
# from src.agent.schemas import AgentDeps, TaskInput
# from src.agent.services import get_todays_tasks
# from src.dependency import user_dependecy, db_dependency
# from src.agent.ai_agent import plannner_agent
# from pydantic_ai import RunContext
#
# # TODO: function to fetch to days date task eg if today is 2023-07-07 then return 2023-07-06 data from db
#
#
# async def get_tasks(ctx: RunContext[AgentDeps]):
#     # check if ther user id exist
#     deps = ctx.deps
#     user_id = deps.user_id
#     db = deps.db
#     if not user_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
#         )
#     # lets fetch all tasks which there created at date is equal to yesterday
#
#     return await get_todays_tasks(user_id, db)

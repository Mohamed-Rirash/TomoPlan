from fastapi import APIRouter, HTTPException, status
from src.agent.ai_agent import plannner_agent
from src.dependency import user_dependecy, db_dependency
from src.agent.schemas import AgentDeps

router = APIRouter()


@router.get("/")
async def read_from_agent(user: user_dependecy, db: db_dependency):
    user_id = user.id  # type: ignore
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    deps = AgentDeps(user_id=user_id, db=db)

    result = await plannner_agent.run(
        "based on my task in that tool iwant to plan my day tasks",
        deps=deps,  # ✅ pass full deps here!
    )

    return result.output

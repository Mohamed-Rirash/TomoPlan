from fastapi import APIRouter
from src.agent.ai_agent import get_plan

router = APIRouter()


@router.get("/")
async def read_from_agent():
    return await get_plan(
        """
                "id": "jadfasdlfjufasdyasdu",
                "task_name": "create fastapi app",
                "task_description": "create a fastapi todo app with sqlalchemy core database to learn and practice crud with them",
    task two
                "id": "jadfasdlfjufasdyasdu",
                "task_name": "wash the clothes",
                "task_description": "wash may clothes and clean the house",
    task three
                "id": "jadfasdlfjufasdyasdu",
                "task_name": "watch a movie",
                "task_description": "watch a movie for intertainment and relaxation",
    """
    )

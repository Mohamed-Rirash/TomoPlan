from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider

from src.agent.prompts import ROAST_PROMPT, SYSTEM_PROMPT
from src.agent.schemas import AgentDeps, Taskoutput
from src.agent.services import get_todays_tasks
from src.config import settings

model = GeminiModel(
    settings.GEMENAI_MODEL, provider=GoogleGLAProvider(api_key=settings.GEMENAI_API_KEY)
)


plannner_agent = Agent(
    model=model,
    output_type=list[Taskoutput],
    system_prompt=SYSTEM_PROMPT,
    output_retries=3,
    deps_type=AgentDeps,
)

# return result.output


# INFO: THIS is tool to get high level of main task definitions with short description to feed the agent
@plannner_agent.tool  # pyright: ignore[reportArgumentType]
async def get_tasks(ctx: RunContext) -> str:
    db = ctx.deps.db  # type: ignore
    tasks = await get_todays_tasks(db)
    return str(tasks)


roast_agent = Agent(
    model=model,
    output_type=str,
    system_prompt=ROAST_PROMPT,
    output_retries=1,
)

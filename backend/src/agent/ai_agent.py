from os import system
from typing import Dict, List
from pydantic_ai import Agent
from src.config import settings
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from loguru import logger
from src.agent.prompt import SYSTEM_PROMPT

model = GeminiModel(
    settings.GEMENAI_MODEL, provider=GoogleGLAProvider(api_key=settings.GEMENAI_API_KEY)
)


async def get_plan(task: str):
    agent = Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
    )
    result = await agent.run(task)
    return result.output

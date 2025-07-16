# middlewares.py
import asyncio
from typing import Any

from limits import parse_many
from limits.storage import RedisStorage
from limits.strategies import FixedWindowRateLimiter
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.config import settings


class LoguruExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)

        except Exception as exc:
            logger.error(
                "❌ Unhandled Exception\n"
                f"➡️ URL: {request.url}\n"
                f"➡️ Method: {request.method}\n"
                f"➡️ Error: {type(exc).__name__}: {exc}"
            )
            return Response(
                content='{"detail": "Internal server error"}',
                status_code=500,
                media_type="application/json",
            )


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate: str = "5/minute"):
        super().__init__(app)
        self._rate_str = rate
        self._limiter: FixedWindowRateLimiter | None = None
        self._storage: RedisStorage | None = None
        self._rate_item = None
        self._lock = asyncio.Lock()

    async def _ensure_limiter(self) -> None:
        if self._limiter is None:
            async with self._lock:
                if self._limiter is None:
                    self._rate_item = parse_many(self._rate_str)[0]
                    redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
                    self._storage = RedisStorage(redis_url)
                    self._limiter = FixedWindowRateLimiter(self._storage)

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        await self._ensure_limiter()

        client_ip = request.client.host
        identifier = f"ratelimit:{client_ip}:{request.url.path}"

        if not self._limiter.test(self._rate_item, identifier):
            return Response(
                content='{"detail": "Rate Limit Exceeded"}',
                status_code=429,
                media_type="application/json",
            )

        self._limiter.hit(self._rate_item, identifier)
        return await call_next(request)

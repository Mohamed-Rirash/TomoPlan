# middlewares/logger_middleware.py

import traceback

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class LoguruExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except Exception as exc:
            # 🔴 Log the full stacktrace + request info
            logger.opt(exception=False).error(
                "❌ Unhandled Exception\n"
                f"➡️ URL: {request.url}\n"
                f"➡️ Method: {request.method}\n"
                f"➡️ Error: {type(exc).__name__}: {str(exc)}"
            )
            # 🔁 Return fallback response
            return Response(
                content='{"detail": "Internal server error"}',
                status_code=500,
                media_type="application/json",
            )


# src/middlewares/rate_limiter.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from limits.storage import RedisStorage
from limits.strategies import FixedWindowRateLimiter
from slowapi.errors import RateLimitExceeded
from loguru import logger
import os

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate: str = "5/minute"):
        super().__init__(app)
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.storage = RedisStorage(redis_url)
        self.limiter = FixedWindowRateLimiter(self.storage)
        self.rate = rate

    async def dispatch(self, request: Request, call_next):
        # 🔑 Rate key: per-IP
        client_ip = request.client.host
        identifier = f"ratelimit:{client_ip}:{request.url.path}"

        try:
            if not self.limiter.test(self.rate, identifier):  # pyright: ignore[reportArgumentType]
                raise RateLimitExceeded("Rate limit exceeded")  # pyright: ignore[reportArgumentType]

            # Consume the token
            self.limiter.hit(self.rate, identifier)  # pyright: ignore[reportArgumentType]

            return await call_next(request)

        except RateLimitExceeded as exc:
            logger.opt(exception=False).error(
                "❌ Rate Limit Exceeded\n"
                f"➡️ URL: {request.url}\n"
                f"➡️ Method: {request.method}\n"
                f"➡️ IP: {client_ip}\n"
                f"➡️ Error: {type(exc).__name__}: {str(exc)}"
            )
            return Response(
                content='{"detail": "Rate Limit Exceeded"}',
                status_code=429,
                media_type="application/json",
            )


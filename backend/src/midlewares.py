# middlewares/logger_middleware.py


from limits.storage import RedisStorage
from limits.strategies import FixedWindowRateLimiter
from loguru import logger
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.config import settings


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


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate: str = "5/minute"):
        super().__init__(app)
        redis_url = settings.REDIS_HOST_URL
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

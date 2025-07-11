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



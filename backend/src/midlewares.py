# middlewares/logger_middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from loguru import logger
import traceback


class LoguruExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except Exception as exc:
            # 🔴 Log the full stacktrace + request info
            logger.opt(exception=False).error(
                f"❌ Unhandled Exception\n"
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

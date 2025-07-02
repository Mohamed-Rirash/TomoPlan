from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter, Request
from src.notifications.notification_stream import NotificationBroadcaster

router = APIRouter()


@router.get("/notifications/stream")
async def notifications_stream(request: Request):
    broadcaster = NotificationBroadcaster()

    async def event_generator():
        async for message in broadcaster.listen():
            yield {"data": message}

    return EventSourceResponse(event_generator())

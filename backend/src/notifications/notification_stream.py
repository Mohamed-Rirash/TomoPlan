# src/notification_stream.py
import asyncio


class NotificationBroadcaster:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def push(self, message: str):
        await self.queue.put(message)

    async def listen(self):
        while True:
            msg = await self.queue.get()
            yield msg

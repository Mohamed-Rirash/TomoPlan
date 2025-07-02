# src/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.notifications.notification_stream import NotificationBroadcaster

# Create a single instance of NotificationBroadcaster that will be used by all scheduled jobs
broadcaster = NotificationBroadcaster()
scheduler = AsyncIOScheduler()


async def schedule_reminders():
    # scheduler.add_job(push_notification, "cron", hour=22, minute=0)  # 10PM
    scheduler.add_job(push_notification, "cron", hour=16, minute=58)  # 4:30 PM
    scheduler.start()


async def push_notification():
    message = (
        "Hey! Reminder to to write down atleast 3 task to accomplish  tomorrow  💪"
    )
    await broadcaster.push(message)
    print("📢 Notification pushed")
    print(message)

import os
from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
app = Celery("agentic_ai_tender", broker=redis_url, backend=redis_url)
app.conf.task_routes = {
    "jobs.tasks.process_tender": {"queue": "analysis"},
    "jobs.tasks.send_notification": {"queue": "notifications"},
}

# Load task modules to ensure tasks are registered with the Celery app.
import jobs.tasks  # noqa: F401

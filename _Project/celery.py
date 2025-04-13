from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_Project.settings')
app = Celery('_Project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks('App')

app.conf.beat_schedule = {
    "archive-sailed-vessels": {
        "task": "App.task.transfer_sailed_vessels_task",
        "schedule": crontab(hour=23, minute=59),  # Runs at 11:59 PM daily
    },
}
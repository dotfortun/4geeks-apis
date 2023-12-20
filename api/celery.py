"""
https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
"""
import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'api.settings'
)

# you can change the name here
app = Celery("fourgeeks_api")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover and load tasks.py from from all registered Django apps
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'clean-old-todos': {
        'task': 'todoapi.tasks.clean_todos',
        'schedule': crontab(minute=0, hour='*/3'),
    }
}
app.conf.timezone = 'UTC'

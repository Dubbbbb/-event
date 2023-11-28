from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events_monitoring.settings')

app = Celery('events_monitoring')
# app = Celery('events_monitoring',
#              broker='redis://redis:6379/0',
#              backend='redis://redis:6379/0',
#              include=['events.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

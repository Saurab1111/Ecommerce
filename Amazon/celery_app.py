import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Amazon.settings')

app = Celery('Amazon')

# Use Django's settings file for config
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()
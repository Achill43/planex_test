import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planex_test.settings')

app = Celery('planex_test')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

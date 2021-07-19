import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planex_test.settings')

app = Celery(
    'planex_test',
    broker="redis://:p8b4cfe5e06377ca95a069555cfb166daaa11d1c037033a0f0fde1fcb8f8301c9@ec2-44-194-38-94.compute-1.amazonaws.com:10540")
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

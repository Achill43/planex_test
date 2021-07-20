import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planex_test.settings')

app = Celery('planex_test')
app.config_from_object('django.conf:settings')

app.conf.update(
    BROKER_URL=os.environ.get(
        'REDIS_URL', 'redis://:p8b4cfe5e06377ca95a069555cfb166daaa11d1c037033a0f0fde1fcb8f8301c9@ec2-44-194-38-94.compute-1.amazonaws.com:10540'),
    CELERY_RESULT_BACKEND=os.environ.get(
        'REDIS_URL', 'redis://:p8b4cfe5e06377ca95a069555cfb166daaa11d1c037033a0f0fde1fcb8f8301c9@ec2-44-194-38-94.compute-1.amazonaws.com:10540'),
    BROKER_POOL_LIMIT=None
)

app.autodiscover_tasks()

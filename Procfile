web: gunicorn planex_test.wsgi --log-file -
worker: celery -A planex_test worker
beat: celery -A planex_test beat
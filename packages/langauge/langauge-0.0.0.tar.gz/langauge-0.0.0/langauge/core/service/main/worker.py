import os

from celery import Celery

env = os.environ
CELERY_BROKER_URL = env.get('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = env.get("CELERY_RESULT_BACKEND", "mongodb://root:root@localhost:27017/celery")

celery = Celery('task',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

celery_app = Celery('core', backend='redis://localhost', broker='redis://localhost:6378/0')

celery_app.conf.result_backend = f"rpc://redis:6378/3"
celery_app.conf.timezone = 'Asia/Tehran'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.task_always_eager = False
celery_app.conf.worker_prefetch_multiplier = 1
celery_app.autodiscover_tasks(['couriers.tasks'])

celery_app.conf.beat_schedule = {
    'create_daily_earning': {
        'task': 'couriers.tasks.create_daily_earning',
        'schedule': crontab(hour=0, minute=1)  # 00:01 of every night
    },
    'create_weakly_earning': {
        'task': 'couriers.tasks.create_weakly_earning',
        'schedule': crontab(day_of_week='saturday', hour=0, minute=5)  # every saturday 00:05
    },
}

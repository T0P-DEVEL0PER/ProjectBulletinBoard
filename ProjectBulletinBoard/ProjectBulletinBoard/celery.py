import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjectBulletinBoard.settings')

app = Celery('ProjectBulletinBoard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'autodelete_one_time_codes': {
        'task': 'key_app.tasks.autodelete_one_time_codes',
        'schedule': 1,
    },
}

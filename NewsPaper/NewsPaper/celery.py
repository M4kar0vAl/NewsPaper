import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'new_posts_weekly': {
        'task': 'news.tasks.week_post_list',
        'schedule': crontab(day_of_week='mon', hour='8', minute='0'),
    },
}

app.autodiscover_tasks()
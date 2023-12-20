import logging
from datetime import timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category

logger = logging.getLogger(__name__)


def week_post_list():
    one_week_ago = timezone.now() - timedelta(days=7)
    last_week_posts = Post.objects.filter(created__gte=one_week_ago)
    categories = Category.objects.filter(posts__post__in=last_week_posts).distinct()
    emails_n_usernames = User.objects.filter(
        subscriptions__category__in=categories
    ).distinct().values('email', 'username')
    subject = 'Новые посты за неделю'
    nl = '\n'
    for obj in emails_n_usernames:
        cur_categories = Category.objects.filter(subscriptions__user__email=obj['email'], id__in=categories)
        posts_to_send = Post.objects.filter(category__in=cur_categories, id__in=last_week_posts).distinct()

        text = f'''Здравствуйте, {obj['username']}!\n
Мы собрали для Вас посты, опубликованные за прошедшую неделю:\n\n
{f'{nl}{nl}'.join([f"{post.heading}{nl}Ссылка на пост: http://127.0.0.1:8000{post.get_absolute_url()}" for post in posts_to_send])}\n'''

        html = f'''Здравствуйте, <b>{obj['username']}</b>!<br>
Мы собрали для Вас посты, опубликованные за прошедшую неделю:<br><br>
<ul>{''.join([f"<li><a href='http://127.0.0.1:8000{post.get_absolute_url()}'><b>{post.heading}</b></a></li>" for post in posts_to_send])}</ul><br>'''

        msg = EmailMultiAlternatives(subject=subject, body=text, from_email=None, to=[obj['email']])
        msg.attach_alternative(html, 'text/html')
        msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            week_post_list,
            trigger=CronTrigger(minute="00", hour="18", day_of_week='fri'),
            id="week_post_list",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'week_post_list'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

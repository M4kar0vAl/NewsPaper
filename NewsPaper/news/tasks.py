from datetime import timedelta

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from news.models import Post, Category


@shared_task
def new_post_notification(id):
    instance = Post.objects.get(id=id)
    pk_set = Category.objects.filter(posts__post__id=id)

    emails_n_usernames = User.objects.filter(
        subscriptions__category__in=pk_set
    ).distinct().values('email', 'username')

    subject = f'Этот пост может быть Вам интересен!'
    nl = '\n'
    for obj in emails_n_usernames:
        text_content = (
            f'''Здравствуйте, {obj['username']}!\
                \nВы получили это письмо, так как подписаны на одну из этих категорий:\n\n{nl.join([str(cat) for cat in instance.category.all()])}\
                \n\nНа сайте опубликован новый пост!\
                \n\n{instance.heading}\
                \n\n{instance.preview()}\
                \n\nСсылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'''
        )
        html_content = (
            f'''Здравствуйте, <b>{obj['username']}</b>!<br>
Вы получили это письмо, так как подписаны на одну из этих категорий:<br><br>{'<br>'.join([f"<b>{str(cat)}</b>" for cat in instance.category.all()])}<br><br>
На <a href='http://127.0.0.1:8000/news'>сайте</a> опубликован новый
<a href='http://127.0.0.1:8000{instance.get_absolute_url()}'>пост</a>!<br><br>
{instance.heading}<br><br>
{instance.preview()}'''
        )
        msg = EmailMultiAlternatives(subject, text_content, None, [obj['email']])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
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
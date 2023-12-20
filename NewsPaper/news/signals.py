from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post


@receiver(m2m_changed, sender=Post.category.through)
def post_category_changed(action, pk_set, instance, **kwargs):
    if action != 'post_add':
        return None

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
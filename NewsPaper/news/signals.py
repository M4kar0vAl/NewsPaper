from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post
from .tasks import new_post_notification


@receiver(m2m_changed, sender=Post.category.through)
def post_category_changed(action, instance, **kwargs):
    if action == 'post_add':
        new_post_notification.delay(
            id=instance.id,
        )
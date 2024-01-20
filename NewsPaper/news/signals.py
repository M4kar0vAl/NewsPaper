from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .models import Post
from .tasks import new_post_notification


@receiver(post_save, sender=Post)
def new_post_handler(instance, created, **kwargs):
    instance.is_new = created


@receiver(m2m_changed, sender=Post.category.through)
def post_category_changed(action, instance, **kwargs):
    if action == 'post_add' and instance.is_new:
        new_post_notification.delay(
            id=instance.id,
        )

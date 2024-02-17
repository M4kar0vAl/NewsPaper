from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('username'))
    rating = models.IntegerField(default=0, verbose_name=_('rating'))

    def update_rating(self):
        post_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        auth_comms_rating = Comment.objects.filter(user=self.user).aggregate(acr=Coalesce(Sum('rating'), 0))['acr']
        post_comms_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'), 0))['pcr']
        self.rating = post_rating * 3 + auth_comms_rating + post_comms_rating
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name=pgettext_lazy('category name', 'name'))

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    ARTICLE = 'ar'
    NEWS = 'nw'
    TYPE = [
        (ARTICLE, _('Article')),
        (NEWS, _('News'))
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('author'))
    type = models.CharField(max_length=2,
                            choices=TYPE,
                            default=NEWS,
                            verbose_name=_('type'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('published'))
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name=_('category'))
    heading = models.CharField(max_length=200, verbose_name=_('heading'))
    text = models.TextField(verbose_name=pgettext_lazy('content of the article', 'content'))
    rating = models.IntegerField(default=0, verbose_name=_('rating'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def __str__(self):
        return f'{self.heading}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             verbose_name=pgettext_lazy('article posted on the website', 'post'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    text = models.TextField(verbose_name=pgettext_lazy('comment text', 'text'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('published'))
    rating = models.IntegerField(default=0, verbose_name=_('rating'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name=_('user')
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name=_('category')
    )

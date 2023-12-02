from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'heading': ['icontains'],
            'category': ['exact'],
            'created': ['gt']
        }
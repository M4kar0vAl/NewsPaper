from django.forms import DateTimeInput
from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateTimeFilter
from .models import Post, Category


class PostFilter(FilterSet):
    heading = CharFilter(
        lookup_expr='iregex',
        label='Заголовок содержит'
    )
    category = ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Выберите категорию'
    )
    created = DateTimeFilter(
        lookup_expr='gt',
        widget=DateTimeInput({'type': 'date'}),
        label='Опубликовано не раньше',
    )

    class Meta:
        model = Post
        fields = ['heading', 'category', 'created']
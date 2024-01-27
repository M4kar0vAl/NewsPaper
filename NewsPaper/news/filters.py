from django.forms import DateTimeInput, TextInput, SelectMultiple
from django_filters import FilterSet, ModelMultipleChoiceFilter, CharFilter, DateTimeFilter
from .models import Post, Category


class PostFilter(FilterSet):
    heading = CharFilter(
        lookup_expr='icontains',
        label='Заголовок содержит',
        widget=TextInput(attrs={'class': 'form-control mb-2 mt-2 text-bg-dark'}),
    )
    category = ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория',
        widget=SelectMultiple(attrs={'class': 'form-select mb-2 mt-2 text-bg-dark'}),
    )
    created = DateTimeFilter(
        lookup_expr='gt',
        widget=DateTimeInput(attrs={'type': 'date', 'class': 'form-control mb-2 mt-2 text-bg-dark'}),
        label='Опубликовано не раньше',
    )

    class Meta:
        model = Post
        fields = ['heading', 'category', 'created']
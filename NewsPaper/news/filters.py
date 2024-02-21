from django.forms import DateTimeInput, TextInput, SelectMultiple
from django_filters import FilterSet, ModelMultipleChoiceFilter, CharFilter, DateTimeFilter
from .models import Post, Category
from django.utils.translation import gettext_lazy as _


class PostFilter(FilterSet):
    heading = CharFilter(
        lookup_expr='icontains',
        label=_('Title contains'),
        widget=TextInput(attrs={'class': 'form-control mb-2 mt-2 text-bg-dark'}),
    )
    category = ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        label=_('Categories'),
        widget=SelectMultiple(attrs={'class': 'form-select mb-2 mt-2 text-bg-dark'}),
    )
    created = DateTimeFilter(
        lookup_expr='gt',
        widget=DateTimeInput(attrs={'type': 'date', 'class': 'form-control mb-2 mt-2 text-bg-dark'}),
        label=_('Published later than'),
    )

    class Meta:
        model = Post
        fields = ['heading', 'category', 'created']

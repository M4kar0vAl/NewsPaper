from django import forms
from django.forms import ModelForm, Textarea
from .models import Post, Category, Author
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy


class NewsForm(ModelForm):
    heading = forms.CharField(label=_('Heading'),
                              widget=forms.TextInput(attrs={'class': 'form-control mb-2 mt-2 text-bg-dark'}))
    text = forms.Field(
        widget=Textarea(
            attrs={
                'class': 'form-control mb-2 mt-2 text-bg-dark',
                'style': 'height: 250px; width: 600px'
            }
        ),
        label=pgettext_lazy('content of the article', 'Content')
    )
    category = forms.ModelMultipleChoiceField(
        label=_('Category'),
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select mb-2 mt-2 text-bg-dark'})
    )

    class Meta:
        model = Post
        fields = [
            'heading',
            'text',
            'category',
        ]

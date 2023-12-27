from django import forms
from django.forms import ModelForm, Textarea
from .models import Post, Category, Author


class NewsForm(ModelForm):
    heading = forms.CharField(label='Heading', widget=forms.TextInput(attrs={'class': 'form-control mb-2 mt-2 text-bg-dark'}))
    text = forms.Field(
        widget=Textarea(
            attrs={
                'class': 'form-control mb-2 mt-2 text-bg-dark',
                'style': 'height: 250px; width: 600px'
            }
        ),
        label='Text'
    )
    category = forms.ModelMultipleChoiceField(
        label='Category',
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select mb-2 mt-2 text-bg-dark'})
    )
    author = forms.ModelChoiceField(
        label='Author',
        queryset=Author.objects.all(),
        empty_label='Выберите автора',
        widget=forms.Select(attrs={'class': 'form-select mb-2 mt-2 text-bg-dark'}),
    )

    class Meta:
        model = Post
        fields = [
            'heading',
            'text',
            'category',
            'author'
        ]

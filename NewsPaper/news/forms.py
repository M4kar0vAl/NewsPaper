from django import forms
from django.forms import ModelForm, Textarea
from .models import Post, Category, Author


class NewsForm(ModelForm):
    heading = forms.CharField(label='Заголовок')
    text = forms.Field(widget=Textarea, label='Текст')
    category = forms.ModelMultipleChoiceField(
        label='Категория',
        queryset=Category.objects.all(),
    )
    author = forms.ModelChoiceField(
        label='Автор',
        queryset=Author.objects.all(),
        empty_label='Выберите автора'
    )

    class Meta:
        model = Post
        fields = [
            'heading',
            'text',
            'category',
            'author'
        ]

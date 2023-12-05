from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import NewsForm
from .models import Post
from .filters import PostFilter


class PostsList(ListView):
    model = Post
    ordering = '-created'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = '-created'
    template_name = 'post_search.html'
    context_object_name = 'filtered_posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs if self.request.GET else Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'nw'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.type = 'ar'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def get_queryset(self):
        news = Post.objects.filter(type='nw')
        return news


class ArticleUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def get_queryset(self):
        articles = Post.objects.filter(type='ar')
        return articles


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        news = Post.objects.filter(type='nw')
        return news


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        articles = Post.objects.filter(type='ar')
        return articles

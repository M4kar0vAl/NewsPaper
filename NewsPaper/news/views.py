from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

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


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = Post.NEWS
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.type = Post.ARTICLE
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def get_queryset(self):
        news = Post.objects.filter(type=Post.NEWS)
        return news


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def get_queryset(self):
        articles = Post.objects.filter(type=Post.ARTICLE)
        return articles


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        news = Post.objects.filter(type=Post.NEWS)
        return news


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        articles = Post.objects.filter(type=Post.ARTICLE)
        return articles

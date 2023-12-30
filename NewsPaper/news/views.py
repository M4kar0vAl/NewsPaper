from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache

from .forms import NewsForm
from .models import Post, Category, Subscriber
from .filters import PostFilter


class PostsList(ListView):
    model = Post
    ordering = '-created'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            context['cats_with_subscriptions'] = Category.objects.annotate(
                user_subscribed=Exists(
                    Subscriber.objects.filter(
                        user=self.request.user,
                        category=OuterRef('pk'),
                    )
                )
            ).order_by('name')
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            context['cats_with_subscriptions'] = Category.objects.annotate(
                user_subscribed=Exists(
                    Subscriber.objects.filter(
                        user=self.request.user,
                        category=OuterRef('pk'),
                    )
                )
            ).order_by('name')
        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object()
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


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
        if self.request.user.is_authenticated:
            context['cats_with_subscriptions'] = Category.objects.annotate(
                user_subscribed=Exists(
                    Subscriber.objects.filter(
                        user=self.request.user,
                        category=OuterRef('pk'),
                    )
                )
            ).order_by('name')
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
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


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        cache.delete('cats_w_subs')
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(user=request.user, category=category).delete()

    categories_with_subscriptions = cache.get('cats_w_subs', None)
    if categories_with_subscriptions is None:
        categories_with_subscriptions = Category.objects.annotate(
            user_subscribed=Exists(
                Subscriber.objects.filter(
                    user=request.user,
                    category=OuterRef('pk'),
                )
            )
        ).order_by('name')
        cache.set('cats_w_subs', categories_with_subscriptions)

    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

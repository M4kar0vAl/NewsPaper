from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Value
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from .forms import NewsForm
from .models import Post, Category, Subscriber, Author
from .filters import PostFilter
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer


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

    def get_queryset(self):
        posts = super().get_queryset()
        if self.request.user.is_authenticated and Author.objects.filter(user=self.request.user).exists():
            posts = posts.annotate(is_owner=Exists(posts.filter(pk=OuterRef('pk'), author=self.request.user.author)))
        else:
            posts = posts.annotate(is_owner=Value(False))
        return posts


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

        obj.is_owner = self.request.user == obj.author.user
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
        filtered_posts = self.filterset.qs
        if self.request.GET:
            if self.request.user.is_authenticated and Author.objects.filter(user=self.request.user).exists():
                filtered_posts = filtered_posts.annotate(
                    is_owner=Exists(filtered_posts.filter(pk=OuterRef('pk'), author=self.request.user.author)))
            else:
                filtered_posts = filtered_posts.annotate(is_owner=Value(False))
            return filtered_posts
        else:
            return Post.objects.none()

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
        try:
            author = Author.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            author = Author.objects.create(user=self.request.user)
        news = form.save(commit=False)
        news.type = Post.NEWS
        news.author = author
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        try:
            author = Author.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            author = Author.objects.create(user=self.request.user)
        article = form.save(commit=False)
        article.type = Post.ARTICLE
        article.author = author
        return super().form_valid(form)


class NewsUpdate(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def test_func(self):
        if self.request.user == self.get_object().author.user:
            self.permission_required = ()
            return True
        elif self.request.user.has_perms(self.permission_required):
            return True
        return False

    def get_queryset(self):
        news = Post.objects.filter(type=Post.NEWS)
        return news


class ArticleUpdate(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def test_func(self):
        if self.request.user == self.get_object().author.user:
            self.permission_required = ()
            return True
        elif self.request.user.has_perms(self.permission_required):
            return True
        return False

    def get_queryset(self):
        articles = Post.objects.filter(type=Post.ARTICLE)
        return articles


class NewsDelete(UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        if self.request.user == self.get_object().author.user:
            self.permission_required = ()
            return True
        elif self.request.user.has_perms(self.permission_required):
            return True
        return False

    def get_queryset(self):
        news = Post.objects.filter(type=Post.NEWS)
        return news


class ArticleDelete(UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        if self.request.user == self.get_object().author.user:
            self.permission_required = ()
            return True
        elif self.request.user.has_perms(self.permission_required):
            return True
        return False

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


class PostAPIListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class NewsViewSet(ModelViewSet):
    queryset = Post.objects.filter(type=Post.NEWS)
    serializer_class = PostSerializer
    pagination_class = PostAPIListPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created', 'rating']
    ordering = ['-created']
    filterset_class = PostFilter

    def get_permissions(self):
        if self.request.user.is_staff:
            self.permission_classes = [IsAuthenticated]
            return [permission() for permission in self.permission_classes]
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ('retrieve', 'update', 'partial_update', 'destroy'):
            self.permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        try:
            author = Author.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            author = Author.objects.create(user=self.request.user)
        kwargs = {
            'author': author,
            'type': Post.NEWS
        }
        serializer.save(**kwargs)


class ArticleViewSet(ModelViewSet):
    queryset = Post.objects.filter(type=Post.ARTICLE).order_by('-created')
    serializer_class = PostSerializer
    pagination_class = PostAPIListPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created', 'rating']
    ordering = ['-created']
    filterset_class = PostFilter

    def get_permissions(self):
        if self.request.user.is_staff:
            self.permission_classes = [IsAuthenticated]
            return [permission() for permission in self.permission_classes]
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ('retrieve', 'update', 'partial_update', 'destroy'):
            self.permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        try:
            author = Author.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            author = Author.objects.create(user=self.request.user)
        kwargs = {
            'author': author,
            'type': Post.ARTICLE
        }
        serializer.save(**kwargs)

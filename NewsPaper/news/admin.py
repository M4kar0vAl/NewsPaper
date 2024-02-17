from django.contrib import admin
from .models import Post, Category, Author, Comment, Subscriber
from modeltranslation.admin import TranslationAdmin


def nullify_rating(modeladmin, request, queryset):
    queryset.update(rating=0)


nullify_rating.short_description = 'Nullify rating'


class PostAdmin(admin.ModelAdmin):
    list_display = ('heading', 'author', 'rating', 'type', 'created')
    list_filter = ('author', 'rating', 'type', 'created', 'category__name')
    search_fields = ('author__user__username', 'heading', 'text', 'category__name')
    actions = [nullify_rating]


class PostTranslatedAdmin(PostAdmin, TranslationAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    list_filter = ('user__username',)
    search_fields = ('user__username',)
    actions = [nullify_rating, 'update_rating']

    @admin.action(description='Update rating')
    def update_rating(self, request, queryset):
        for author in queryset:
            author.update_rating()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class CategoryTranslatedAdmin(CategoryAdmin, TranslationAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'rating', 'created')
    list_filter = ('user', 'rating', 'created')
    search_fields = ('user__username', 'text', 'post__heading', 'post__text')
    actions = [nullify_rating]


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')
    list_filter = ('category', 'user')
    search_fields = ('category__name', 'user__username')


admin.site.register(Post, PostTranslatedAdmin)
admin.site.register(Category, CategoryTranslatedAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscriber, SubscriberAdmin)

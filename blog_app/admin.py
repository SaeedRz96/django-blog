from django.contrib.admin import register, ModelAdmin
from .models import *


@register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = ['title', 'owner', 'is_active', 'is_private', 'created_at']
    list_filter = ['is_active', 'is_private', 'created_at']
    search_fields = ['title', 'owner__username', 'owner__email']
    list_per_page = 10
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['authers']
    autocomplete_fields = ['owner']



@register(Post)
class PostAdmin(ModelAdmin):
    list_display = ['title', 'blog', 'author', 'is_active', 'is_private', 'created_at']
    list_filter = ['is_active', 'is_private', 'created_at']
    search_fields = ['title', 'blog__title', 'author__username', 'author__email']
    list_per_page = 10
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['blog', 'author']


@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ['post', 'author',  'created_at']
    list_filter = ['created_at',]
    search_fields = ['post__title', 'author__username', 'author__email', 'content']
    list_per_page = 10
    autocomplete_fields = ['post', 'author']
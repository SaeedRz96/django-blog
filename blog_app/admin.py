from django.contrib.admin import register, ModelAdmin
from .models import *


@register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = ['title', 'owner', 'is_active', 'is_private', 'created_at',]
    list_filter = ['is_active', 'is_private', 'created_at']
    search_fields = ['title', 'owner__username', 'owner__email']
    list_per_page = 10
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['authers']
    autocomplete_fields = ['owner']




@register(Post)
class PostAdmin(ModelAdmin):
    list_display = ['title', 'blog', 'author', 'is_active', 'is_private', 'created_at', 'tag_list']
    list_filter = ['is_active', 'is_private', 'created_at']
    search_fields = ['title', 'blog__title', 'author__username', 'author__email']
    list_per_page = 10
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['blog', 'author']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ['post', 'author',  'created_at']
    list_filter = ['created_at',]
    search_fields = ['post__title', 'author__username', 'author__email', 'content']
    list_per_page = 10
    autocomplete_fields = ['post', 'author']


@register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    list_display = ['blog', 'user', ]
    search_fields = ['blog__title', 'user__username', 'user__email', 'email']
    list_per_page = 10
    autocomplete_fields = ['blog', 'user']


@register(SubscribeRequest)
class SubscribeRequestAdmin(ModelAdmin):
    list_display = ['blog', 'user', ]
    list_filter = ['requested_at','is_deleted','status']
    search_fields = ['blog__title', 'user__username', 'user__email', 'email']
    list_per_page = 10
    autocomplete_fields = ['blog', 'user']


@register(Like)
class LikeAdmin(ModelAdmin):
    list_display = ['post', 'user', 'liked_at']
    list_filter = ['liked_at',]
    search_fields = ['post__title', 'user__username', 'user__email']
    list_per_page = 10
    autocomplete_fields = ['post', 'user']


@register(LikeComment)
class LikeCommentAdmin(ModelAdmin):
    list_display = ['comment', 'user', 'liked_at']
    list_filter = ['liked_at',]
    search_fields = ['comment__post__title', 'user__username', 'user__email']
    list_per_page = 10
    autocomplete_fields = ['comment', 'user']


@register(SavedPost)
class SavedPostAdmin(ModelAdmin):
    list_display = ['post', 'user', 'saved_at']
    list_filter = ['saved_at',]
    search_fields = ['post__title', 'user__username', 'user__email']
    list_per_page = 10
    autocomplete_fields = ['post', 'user']


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name',]
    list_per_page = 10


@register(FollowTag)
class FollowTagAdmin(ModelAdmin):
    list_display = ['tag', 'user', ]
    search_fields = ['tag__name', 'user__username', 'user__email']
    list_per_page = 10
    autocomplete_fields = ['tag', 'user']


@register(Report)
class ReportAdmin(ModelAdmin):
    list_display = ['post', 'user', 'reported_at']
    list_filter = ['reported_at',]
    search_fields = ['post__title', 'user__username', 'user__email', 'content']
    list_per_page = 10
    autocomplete_fields = ['post', 'user', 'comment','reporter', 'blog']
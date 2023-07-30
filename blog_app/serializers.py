from rest_framework.serializers import ModelSerializer,StringRelatedField
from .models import *
from taggit.serializers import (TagListSerializerField,TaggitSerializer)


class BlogSerializer(ModelSerializer):


    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'logo', 'description', 'created_at', 'is_active', 'is_private', 'owner', 'authers', 'posts_count', 'absolute_url']
   

class PostSerializer(TaggitSerializer,ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Post
        fields = ['id', 'blog', 'author', 'title', 'slug', 'content', 'created_at', 'is_active', 'is_private','is_published', 'likes','tags']
    

class CommentSerializer(ModelSerializer):
    likers = StringRelatedField(many=True)
    replies = StringRelatedField(many=True)
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at','likes','likers','replies']


class SubscriberSerializer(ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'


class SubscribeRequestSerializer(ModelSerializer):
    class Meta:
        model = SubscribeRequest
        fields = '__all__'


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class LikeCommentSerializer(ModelSerializer):
    class Meta:
        model = LikeComment
        fields = '__all__'


class SavedPostSerializer(ModelSerializer):
    class Meta:
        model = SavedPost
        fields = '__all__'


class TagSerializer(ModelSerializer):
    followers = StringRelatedField(many=True)
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at', 'posts_count','followers_count','followers']
    

class FollowTagSerializer(ModelSerializer):
    class Meta:
        model = FollowTag
        fields = '__all__'


class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class SeriesSerializer(ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'
        read_only_fields = ['created_at']


class UserBadgeSerializer(ModelSerializer):
    class Meta:
        model = UserBadge
        fields = '__all__'
        read_only_fields = ['date']
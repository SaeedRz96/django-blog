from rest_framework.serializers import ModelSerializer,StringRelatedField
from .models import *


class BlogSerializer(ModelSerializer):


    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'logo', 'description', 'created_at', 'is_active', 'is_private', 'owner', 'authers', 'posts_count', 'absolute_url']
        



class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'blog', 'author', 'title', 'slug', 'content', 'created_at', 'is_active', 'is_private', 'likes']
    

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
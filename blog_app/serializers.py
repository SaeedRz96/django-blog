from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *


class BlogSerializer(ModelSerializer):


    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'logo', 'description', 'created_at', 'is_active', 'is_private', 'owner', 'authers', 'posts_count', 'absolute_url']
        



class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
    

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class SubscriberSerializer(ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'


class SubscribeRequestSerializer(ModelSerializer):
    class Meta:
        model = SubscribeRequest
        fields = '__all__'
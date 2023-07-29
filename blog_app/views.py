from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import *
from .serializers import *


class PostCountOrder(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return sorted(queryset, key=lambda t: t.posts_count, reverse=True)


class BlogList(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, PostCountOrder]
    filterset_fields = ['owner', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
        

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(is_active=True,blog__is_active=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['blog', 'author', 'is_active','tags__name']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # remove posts from private blogs if user is not subscribed
        for post in queryset:
            if post.blog.is_private:
                if not post.blog.subscribers.filter(user=request.user).exists():
                    queryset = queryset.exclude(id=post.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def retrieve(self, request, *args, **kwargs):
        # check if user is subscribed to this blog or blog is not private
        post = self.get_object()
        if post.blog.is_private:
            if not post.blog.subscribers.filter(user=request.user).exists():
                raise ValidationError('This blog is private. make request to subscribe.')
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post', 'author']
    search_fields = ['content']
    ordering_fields = ['created_at']


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class SubscriberList(generics.ListCreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['blog', 'user']
    search_fields = ['email']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        # check blog is not private
        blog = serializer.validated_data['blog']
        if blog.is_private:
            raise ValidationError('This blog is private. make request to subscribe.')
        serializer.save(user=self.request.user)


class SubscriberDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticated]


class SubscribeRequestList(generics.ListCreateAPIView):
    queryset = SubscribeRequest.objects.all()
    serializer_class = SubscribeRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['blog', 'user']
    search_fields = ['email']
    ordering_fields = ['created_at']
    # set status to pending when creating a new subscribe request
    def perform_create(self, serializer):
        serializer.save(status='pending')


class SubscribeRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscribeRequest.objects.all()
    serializer_class = SubscribeRequestSerializer
    permission_classes = [IsAuthenticated]


class LikeList(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post', 'user']
    search_fields = ['user__username']
    ordering_fields = ['liked_at']


class LikeCommentList(generics.ListCreateAPIView):
    queryset = LikeComment.objects.all()
    serializer_class = LikeCommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['comment', 'user']
    search_fields = ['user__username']
    ordering_fields = ['liked_at']
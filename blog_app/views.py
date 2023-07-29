from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError

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
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['blog', 'author', 'is_active']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


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

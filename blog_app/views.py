from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

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
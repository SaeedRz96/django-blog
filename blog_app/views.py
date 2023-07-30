from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

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
    queryset = Post.objects.filter(is_active=True,blog__is_active=True,is_published=True)
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


class SavedPostList(generics.ListCreateAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post', 'user']
    search_fields = ['user__username']
    ordering_fields = ['saved_at']


class TagsPostCountOrder(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return sorted(queryset, key=lambda t: t.posts_count, reverse=True)
    

class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,TagsPostCountOrder]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['created_at','name']


class FollowTagList(generics.ListCreateAPIView):
    queryset = FollowTag.objects.all()
    serializer_class = FollowTagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tag', 'user']
    search_fields = ['user__username']
    ordering_fields = ['followed_at']


class ReportList(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post','comment' ,'user', 'status', 'report_type']
    search_fields = ['user__username']
    ordering_fields = ['reported_at']


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]


class SeriesList(generics.ListCreateAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'is_active']
    search_fields = ['title']
    ordering_fields = ['created_at', 'title']
    def perform_create(self, serializer):
        # check request user is blog owner
        if not self.request.user == serializer.validated_data['author']:
            raise ValidationError('You are not the author of this series.')
        serializer.save(author=self.request.user)


class SeriesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsAuthenticated]
    def perform_update(self, serializer):
        # check request user is blog owner
        if not self.request.user == serializer.validated_data['author']:
            raise ValidationError('You are not the author of this series.')
        serializer.save(author=self.request.user)
    def perform_destroy(self, instance):
        # check request user is blog owner
        if not self.request.user == instance.author:
            raise ValidationError('You are not the author of this series.')
        instance.delete()


class UserBadgeList(generics.ListAPIView):
    queryset = UserBadge.objects.all()
    serializer_class = UserBadgeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'badge']
    search_fields = ['user__username']
    ordering_fields = ['date']


class DraftList(APIView):
    def get(self, request, format=None):
        blog = request.query_params.get('blog', None)
        if blog is not None:
            # check if user is blog owner or in blog authors
            if not request.user == Blog.objects.get(id=blog).owner and not request.user in Blog.objects.get(id=blog).authers.all():
                raise ValidationError('You are not the owner or author of this blog.')
            posts = Post.objects.filter(blog=blog,is_active=True,is_published=False)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)



    
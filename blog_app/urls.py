from blog_app.views import *
from django.urls import path

app_name = 'blog_app'
urlpatterns = [
    path('blog', BlogList.as_view(), name='blogs'),
    path('blog/<int:pk>', BlogDetail.as_view(), name='blog_detail'),
    path('post', PostList.as_view(), name='posts'),
    path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('comment', CommentList.as_view(), name='comments'),
    path('comment/<int:pk>', CommentDetail.as_view(), name='comment_detail'),
    path('subscriber', SubscriberList.as_view(), name='subscribers'),
    path('subscriber/<int:pk>', SubscriberDetail.as_view(), name='subscriber_detail'),
    path('subscribe_request', SubscribeRequestList.as_view(), name='subscribe_requests'),
    path('subscribe_request/<int:pk>', SubscribeRequestDetail.as_view(), name='subscribe_request_detail'),
    path('like', LikeList.as_view(), name='likes'),
    path('like-comment', LikeCommentList.as_view(), name='like_comments'),
    path('saved-post', SavedPostList.as_view(), name='saved_posts'),
    path('tag', TagList.as_view(), name='tags'),
    path('follow-tag', FollowTagList.as_view(), name='follow_tags'),
    path('report', ReportList.as_view(), name='reports'),
    path('report/<int:pk>', ReportDetail.as_view(), name='report_detail'),
]
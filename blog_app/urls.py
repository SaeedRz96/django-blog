from blog_app.views import *
from django.urls import path

app_name = 'blog_app'
urlpatterns = [
    path('blog', BlogList.as_view(), name='blogs'),
    path('blog/<int:pk>/', BlogDetail.as_view(), name='blog_detail'),
    path('post', PostList.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
]
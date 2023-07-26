from user_app.views import *
from django.urls import path

app_name = 'user_app'
urlpatterns = [
    path('auth/check', CheckUserExistsAPIView.as_view()),
    path('auth/register', RegisterAPIView.as_view()),
    path('auth/login', LoginAPIView.as_view()),
    path('auth/verify', UserAPIView.as_view()),
    path('auth/refresh', RefreshAPIView.as_view()),
    path('auth/logout', LogoutAPIView.as_view()),
]
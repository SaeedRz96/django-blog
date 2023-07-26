from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user_app.urls')),
    path('api/blog/', include('blog_app.urls')),
    path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

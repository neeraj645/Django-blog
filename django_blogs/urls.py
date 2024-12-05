from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django_blogs import settings

urlpatterns = [
    path('admin/', admin.site.urls),
     path('users/', include('users.urls')),  # Correct inclusion
    path('', include("blog.urls")),  # Correct inclusion
]

if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

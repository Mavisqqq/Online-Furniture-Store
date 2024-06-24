from django.contrib import admin
from django.urls import path, include
from fursite import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('furniture.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
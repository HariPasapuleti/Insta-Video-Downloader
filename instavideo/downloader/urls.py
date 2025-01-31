from django.urls import path
from .views import download_video
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/download/', download_video, name='download_video'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

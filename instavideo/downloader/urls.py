from django.urls import path
from .views import download_video, test_api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/download/', download_video, name='download_video'),
    path('api/test/', test_api, name='test_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

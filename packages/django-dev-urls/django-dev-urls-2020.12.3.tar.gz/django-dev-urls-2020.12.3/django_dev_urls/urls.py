from django.conf import settings
from django.conf.urls.static import static

urlpatterns = []
if settings.DEBUG:
    if settings.STATIC_URL and settings.STATIC_ROOT:
        urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if settings.MEDIA_URL and settings.MEDIA_ROOT:
        urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

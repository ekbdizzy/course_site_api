from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls', namespace='user')),
    path('api/course/', include('course.urls', namespace='course')),
    path('', include('documentation.urls', namespace='documentation'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

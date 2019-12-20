from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('user.urls', namespace='user')),
    path('api/course/', include('course.urls', namespace='course')),
    path('api/lesson/', include('lesson.urls', namespace='lesson')),
]

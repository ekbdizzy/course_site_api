from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('user.urls', namespace='user')),
    path('course/', include('course.urls', namespace='course')),
    path('lesson/', include('lesson.urls', namespace='lesson')),
]

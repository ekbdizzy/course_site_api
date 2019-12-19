from django.urls import path
from .views import CoursesListView

app_name = 'course'

urlpatterns = [
    path('api/courses', CoursesListView.as_view())
]
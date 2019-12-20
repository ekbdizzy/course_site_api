from django.urls import path
from .views import CoursesListView, CourseDetailView

app_name = 'course'

urlpatterns = [
    path('list/', CoursesListView.as_view()),
    path('detail/<int:pk>/', CourseDetailView.as_view()),
]
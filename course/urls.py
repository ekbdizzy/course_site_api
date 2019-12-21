from django.urls import path
from .views import CoursesListView, CourseDetailView, StudentsOnCourseView

app_name = 'course'

urlpatterns = [
    path('list/', CoursesListView.as_view(), name='list'),
    path('detail/<int:pk>/', CourseDetailView.as_view()),
    path('detail/<int:pk>/students/', StudentsOnCourseView.as_view()),
]

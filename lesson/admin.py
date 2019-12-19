from django.contrib import admin
from .models import Lesson


# Register your models here.
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    list_display = (
        'course',
        'teacher',
        'title',
        'date_and_time',
    )

    list_filter = ('course', 'teacher', 'date_and_time', )

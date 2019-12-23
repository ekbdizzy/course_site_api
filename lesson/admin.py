from django.contrib import admin
from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    list_display = (
        'teacher',
        'title',
        'date_and_time',
    )

    list_filter = ('teacher', 'date_and_time',)

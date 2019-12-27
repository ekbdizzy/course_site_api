from django.contrib import admin
from .models import Lesson
from django import forms
from user.models import User


def get_only_teachers(obj):
    return obj.objects.filter(is_teacher=True)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):

    class Meta:
        model = Lesson
        list_display = (
            'teacher',
            'title',
            'date_and_time',
        )
        widgets = {
            'type': forms.Select()
        }

        list_filter = ('teacher', 'date_and_time',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':
            kwargs['queryset'] = User.objects.filter(is_teacher=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

from django.contrib import admin
from .models import Course, StudentOfCourse


class StudentOfCourseInline(admin.TabularInline):
    model = StudentOfCourse
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = (
        'title',
        'start_date',
        'price',
        'duration',
    )
    list_filter = ('start_date',)

    inlines = (StudentOfCourseInline,)

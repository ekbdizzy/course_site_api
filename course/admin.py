from django.contrib import admin
from .models import Course, StudentOnCourse, LessonOnCourse


class StudentOfCourseInline(admin.TabularInline):
    model = StudentOnCourse
    extra = 1


class LessonOnCourseInline(admin.TabularInline):
    model = LessonOnCourse
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

    inlines = (StudentOfCourseInline, LessonOnCourseInline)

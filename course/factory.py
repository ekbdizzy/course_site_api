from datetime import date
from factory import django, Faker, fuzzy

from lesson.models import Lesson
from user.models import User
from .models import Course, StudentOnCourse, LessonOnCourse

DURATION_CHOICES = (
    '1 month',
    '2 months',
    '3 months',
    '4 months',
    '5 months',
    '6 months',
)

STATUSES_OF_STUDENT = (
    'not started',
    'finished',
    'in progress',
    'failed'
)


class CourseFactory(django.DjangoModelFactory):
    class Meta:
        model = Course

    title = Faker('sentence')
    description = Faker('text')
    start_date = fuzzy.FuzzyDate(date(2019, 1, 1), date(2019, 12, 12))
    price = fuzzy.FuzzyChoice(range(20000, 60000, 2000))
    duration = fuzzy.FuzzyChoice(choices=DURATION_CHOICES)
    icon = django.ImageField(
        width=1000,
        height=1000,
        image_format='png'
    )


class StudentOnCourseFactory(django.DjangoModelFactory):
    class Meta:
        model = StudentOnCourse

    student = fuzzy.FuzzyChoice(User.objects.filter(is_teacher=False))
    course = fuzzy.FuzzyChoice(Course.objects.all())
    course_is_paid = fuzzy.FuzzyChoice((True, False))
    status = fuzzy.FuzzyChoice(choices=STATUSES_OF_STUDENT)


class LessonOnCourseFactory(django.DjangoModelFactory):
    class Meta:
        model = LessonOnCourse

    course = fuzzy.FuzzyChoice(Course.objects.all())
    lesson = fuzzy.FuzzyChoice(Lesson.objects.all())

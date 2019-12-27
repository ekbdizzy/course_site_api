from django.core.management import BaseCommand
from rest_framework.authtoken.models import Token

from user.models import User
from user.factory import UserFactory, TeacherFactory
from lesson.models import Lesson
from lesson.factory import LessonFactory
from course.models import Course, LessonOnCourse, StudentOnCourse
from course.factory import CourseFactory, LessonOnCourseFactory, StudentOnCourseFactory


def create_factory(factory, quantity: int):
    for item in range(quantity):
        factory()


class Command(BaseCommand):

    @staticmethod
    def get_query_set():
        return User.objects.filter(is_superuser=False)

    def handle(self, *args, **options):
        Token.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        LessonOnCourse.objects.all().delete()
        StudentOnCourse.objects.all().delete()

        create_factory(UserFactory, 50)
        create_factory(TeacherFactory, 15)

        for user in User.objects.filter(is_superuser=False):
            user.set_password('1')
            Token.objects.create(user=user)

            user.save()

        create_factory(LessonFactory, 100)
        create_factory(CourseFactory, 10)
        create_factory(LessonOnCourseFactory, 100)
        create_factory(StudentOnCourseFactory, 50)

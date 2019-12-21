from django.db import models
from user.models import User
from lesson.models import Lesson

STATUSES_OF_STUDENT = (
    ('not started', 'not started'),
    ('finished', 'finished'),
    ('in progress', 'in progress'),
    ('failed', 'failed'),
)


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=250, default='')
    description = models.TextField(max_length=2000, default='')
    start_date = models.DateField(auto_created=False, auto_now=False, blank=True)
    price = models.DecimalField(max_digits=6, default=0, decimal_places=0)
    duration = models.CharField(max_length=250)
    students = models.ManyToManyField(User, through='StudentOnCourse', related_name='students')
    lessons = models.ManyToManyField(Lesson, through='LessonOnCourse', related_name='lessons')

    def __str__(self):
        return f"{self.title}: {self.start_date}"


class StudentOnCourse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_from_student')
    course_is_paid = models.BooleanField(default=False)
    status = models.CharField(choices=STATUSES_OF_STUDENT, default='not started', max_length=100)

    def __str__(self):
        return f"Course: {self.course}"


class LessonOnCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_of_lesson')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_on_course')

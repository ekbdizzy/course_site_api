from django.db import models
from user.models import User
from lesson.models import Lesson


class Course(models.Model):

    def image_folder(self, filename):
        image_folder_name = self.title
        filename = '.'.join([image_folder_name, filename.split('.')[-1]])
        return f'course/{image_folder_name}/{filename}'

    title = models.CharField(max_length=250, default='')
    description = models.TextField(max_length=2000, default='')
    start_date = models.DateField(auto_created=False, auto_now=False, blank=True)
    price = models.DecimalField(max_digits=6, default=0, decimal_places=0)
    icon = models.ImageField(upload_to=image_folder, blank=True)
    duration = models.CharField(max_length=250)
    students = models.ManyToManyField(User, through='StudentOnCourse', related_name='students')
    lessons = models.ManyToManyField(Lesson, through='LessonOnCourse', related_name='lessons')

    def __str__(self):
        return f"{self.title}: {self.start_date}"

    def get_students_by_status(self, status):
        return self.students.filter(student__status=status)

    def get_students_paid_for_course(self):
        return self.students.filter(student__course_is_paid=True)


class StudentOnCourse(models.Model):
    STATUSES_OF_STUDENT = (
        ('not started', 'not started'),
        ('finished', 'finished'),
        ('in progress', 'in progress'),
        ('failed', 'failed'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_from_student')
    course_is_paid = models.BooleanField(default=False)
    status = models.CharField(choices=STATUSES_OF_STUDENT, default='not started', max_length=100)

    def __str__(self):
        return f"Course: {self.course}"


class LessonOnCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_of_lesson')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_on_course')

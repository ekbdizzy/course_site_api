from django.db import models
from user.models import User
from django.core.validators import ValidationError


class Lesson(models.Model):

    def clean(self):
        if not self.teacher.is_teacher:
            raise ValidationError('Teacher must have active status is_teacher')
        super().clean()

    date_and_time = models.DateTimeField(auto_now_add=False, auto_created=False, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, validators=())
    title = models.CharField(max_length=250, default='', null=False)
    description = models.TextField(max_length=2000, default='', blank=True)

    def __str__(self):
        return f"{self.date_and_time}: {self.title} - {self.teacher}"

from django.db import models
from user.models import User


class Lesson(models.Model):
    class Meta:
        ordering = ('date_and_time',)

    date_and_time = models.DateTimeField(auto_now_add=False, auto_created=False, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, validators=())
    title = models.CharField(max_length=250, default='', null=False)
    description = models.TextField(max_length=2000, default='', blank=True)

    def __str__(self):
        return f"{self.date_and_time}: {self.title} - {self.teacher}"

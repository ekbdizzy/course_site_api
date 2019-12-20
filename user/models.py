from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from user.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    def image_folder(self, filename):
        image_folder_name = self.email.split('@')[0]
        filename = '.'.join([image_folder_name, filename.split('.')[-1]])
        return f'users/{image_folder_name}/{filename}'

    objects = UserManager()

    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(unique=True, max_length=15, verbose_name='Phone')
    avatar = models.ImageField(upload_to=image_folder, blank=True)
    full_name = models.CharField(max_length=100, blank=True, verbose_name='Full name')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name='Is active')
    is_teacher = models.BooleanField(default=False, verbose_name='Is teacher')
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    is_superuser = models.BooleanField(default=False, verbose_name="Administrator")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    def __str__(self):
        return f'{"Teacher: " if self.is_teacher else ""}{self.full_name}{" - " if self.full_name else ""}{self.email}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('email',)

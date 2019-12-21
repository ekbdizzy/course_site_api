from celery import task
from django.core.mail import send_mail
from django.conf import settings
from .models import User


@task
def user_is_registered_email(email):
    """ Send letter to new users """

    user = User.objects.get(email=email)
    subject = f'You are registered on uur site'
    message = f'{user.full_name}, welcome to our site <a href="https://www.site.ru">site.com</a><br>' \
              f'We are glad to see you here, please, write us if you need help'
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        html_message=message
    )

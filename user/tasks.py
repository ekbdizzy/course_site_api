from celery import task
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from utils.logger import logging


@task
def user_is_registered_email(email):
    """ Send letter to new users """

    site = Site.objects.get_current()

    try:
        user = User.objects.get(email=email)
        subject = f'You are registered on {site.name}'
        message = f'{user.full_name}, welcome to our site <a href="{site.domain}">{site.name}</a><br>' \
                  f'We are glad to see you here, please, write us if you need help'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            html_message=message
        )

    except User.DoesNotExist:
        logging.error(f'User with email {email} not found')

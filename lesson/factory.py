from datetime import datetime
from factory import django, Faker, fuzzy
from pytz import UTC

from user.models import User
from .models import Lesson


class LessonFactory(django.DjangoModelFactory):
    class Meta:
        model = Lesson

    date_and_time = fuzzy.FuzzyDateTime(start_dt=datetime(2019, 1, 1, tzinfo=UTC),
                                        end_dt=datetime(2019, 12, 12, tzinfo=UTC))
    teacher = fuzzy.FuzzyChoice(choices=User.objects.filter(is_teacher=True))
    title = Faker('sentence')
    description = Faker('text')

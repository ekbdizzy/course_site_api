from factory import django, Faker, fuzzy

from .models import User

COLORS = (
    'blue',
    'red',
    'yellow',
    'green',
    'black',
    'orange',
)


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = User

    email = Faker('email')
    avatar = django.ImageField(
        width=1000,
        height=1000,
        color=fuzzy.FuzzyChoice(choices=COLORS)
    )
    full_name = Faker('name')
    is_active = True


class TeacherFactory(UserFactory):
    is_teacher = True

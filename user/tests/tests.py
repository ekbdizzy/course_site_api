import pytest
from django.contrib.auth import authenticate
from user.serializers import UserSerializer
from rest_framework.authtoken.models import Token


@pytest.fixture(scope='module')
def default_user_data():
    return {
        "email": "test@test.com",
        "full_name": 'test_user',
        "password": "1"
    }


@pytest.fixture(scope='function')
def create_default_user(django_user_model, default_user_data):
    user = django_user_model.objects.create_user(
        email=default_user_data['email'],
        full_name=default_user_data['full_name'],
        password=default_user_data['password']
    )
    Token.objects.create(user=user)
    return user


@pytest.fixture(scope='function')
def create_teacher(django_user_model):
    teacher = django_user_model.objects.create_user(
        email="teacher@test.com",
        password='1',
        full_name="teacher",
        is_teacher=True)
    return teacher


def test_auth_user(create_default_user, default_user_data):
    user = authenticate(email=default_user_data['email'], password=default_user_data['password'])
    assert user is not None
    assert user.is_authenticated


def test_image_folder(create_default_user):
    filename = 'example.jpg'
    result = 'users/test/test.jpg'
    assert create_default_user.image_folder(filename) == result


def test_str_student_with_full_name(create_default_user):
    result = 'test_user - test@test.com'
    assert create_default_user.__str__(), result


def test_str_teacher(create_teacher):
    result = 'Teacher: teacher - teacher@test.com'
    assert create_teacher.__str__() == result


def test_UserSerializer(create_default_user, default_user_data):
    serializer = UserSerializer(instance=create_default_user)
    assert serializer.data['email'] == default_user_data['email']
    assert serializer.data['full_name'] == default_user_data['full_name']


@pytest.mark.django_db
def test_UserSerialiser_create(default_user_data):
    serializer = UserSerializer(data=default_user_data)
    user = serializer.create(validated_data=default_user_data)
    assert user.email, default_user_data['email']
    assert user.full_name, default_user_data['full_name']

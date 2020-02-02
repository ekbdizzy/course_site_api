import pytest

from rest_framework import status
from rest_framework.test import APIRequestFactory
from user.views import CreateUserView
from user.serializers import UserSerializer


@pytest.fixture(scope='module')
def default_user_data():
    return {
        "email": "test@test.com",
        "full_name": 'test_user',
        "password": "1"
    }


def test_serializer_is_valid(default_user_data):
    serializer = UserSerializer(data=default_user_data)
    serializer.is_valid()
    email = serializer.validated_data['email']
    full_name = serializer.validated_data['full_name']
    password = serializer.validated_data['password']

    assert email == default_user_data['email']
    assert full_name == default_user_data['full_name']
    assert password == default_user_data['password']


@pytest.mark.django_db
def test_CreateUserView_valid(default_user_data):
    view = CreateUserView.as_view()
    factory = APIRequestFactory()

    request = factory.post('/api/user/register', data=default_user_data)
    response = view(request)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_CreateUserView_user_is_already_registered(django_user_model, default_user_data):
    view = CreateUserView.as_view()
    factory = APIRequestFactory()

    django_user_model.objects.create(
        email="test@test.com",
        password='1',
        full_name="test_user"
    )

    request = factory.post('/api/user/register', data=default_user_data)
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['message'] == 'Email is already registered'


@pytest.mark.django_db
def test_CreateUserView_invalid_data(default_user_data):
    view = CreateUserView.as_view()
    factory = APIRequestFactory()

    data = {
        "full_name": default_user_data['full_name'],
        "password": default_user_data['password']
    }

    request = factory.post('/api/user/register', data=data)
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

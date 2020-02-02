import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient

from user.views import AuthenticateUserView


@pytest.fixture(scope='module')
@pytest.mark.django_db
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


@pytest.mark.django_db
def test_user_login(create_default_user):
    url = reverse('user:login')
    data = {"email": "test@test.com",
            "password": "1"}

    user = create_default_user
    client = APIClient()
    response = client.post(url, data, format='json')
    print(response.status_code)

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.data['email'] == user.email


@pytest.mark.django_db
def test_user_does_not_exists():
    url = reverse('user:login')
    view = AuthenticateUserView.as_view()

    data = {
        "email": "wrong_email@test.com",
        "password": "1"
    }
    factory = APIRequestFactory()
    request = factory.post(url, data, format='json')
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['message'] == "User is not registered"


@pytest.mark.django_db
def test_user_password_is_incorrect(create_default_user):
    url = reverse('user:login')
    view = AuthenticateUserView.as_view()

    data = {
        "email": "test@test.com",
        "password": "2"
    }

    factory = APIRequestFactory()
    request = factory.post(url, data=data)
    response = view(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['message'] == "Password is incorrect"

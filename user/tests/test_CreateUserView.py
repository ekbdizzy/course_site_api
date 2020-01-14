from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from user.views import CreateUserView

from user.serializers import UserSerializer
from user.models import User


class CreateUserViewTest(TestCase):

    def tearDown(self):
        try:
            User.objects.get(email="test@test.com").delete()
        except User.DoesNotExist:
            pass

    def test_serializer_is_valid(self):
        data = {
            "email": "test@test.com",
            "full_name": 'test_user',
            "password": "1"
        }
        serializer = UserSerializer(data=data)
        serializer.is_valid()
        email = serializer.validated_data['email']
        full_name = serializer.validated_data['full_name']
        password = serializer.validated_data['password']

        self.assertTrue(
            email == data['email'] and full_name == data['full_name'] and password == data['password']
        )

    def test_CreateUserView_valid(self):
        view = CreateUserView.as_view()
        factory = APIRequestFactory()

        data = {
            "email": "test@test.com",
            "full_name": 'test_user',
            "password": "1"
        }

        request = factory.post('/api/user/register', data=data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_CreateUserView_user_is_already_registered(self):

        view = CreateUserView.as_view()
        factory = APIRequestFactory()

        user = User.objects.create(
            email="test@test.com",
            password='1',
            full_name="test_user"
        )

        data = {
            "email": "test@test.com",
            "full_name": 'test_user',
            "password": "1"
        }

        request = factory.post('/api/user/register', data=data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_CreateUserView_invalid_data(self):

        view = CreateUserView.as_view()
        factory = APIRequestFactory()

        data = {
            "full_name": 'test_user',
            "password": "1"
        }

        request = factory.post('/api/user/register', data=data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

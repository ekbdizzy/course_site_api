from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from user.views import AuthenticateUserView


class AuthenticateUserViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password='1',
            full_name="test_user"
        )
        self.user.save()
        token = Token.objects.create(user=self.user)

    def tearDown(self) -> None:
        self.user.delete()

    def test_user_login(self):
        url = reverse('user:login')
        data = {
            "email": "test@test.com",
            "password": "1"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_user_does_not_exists(self):
        url = reverse('user:login')
        data = {
            "email": "test11@test.com",
            "password": "1"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "User is not registered")

    def test_user_password_is_incorrect(self):
        url = reverse('user:login')
        data = {
            "email": "test@test.com",
            "password": "2"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Password is incorrect")

from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase

from user.serializers import UserSerializer
from user.models import User


class UserModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password='1',
            full_name="test_user"
        )
        self.user.save()

        self.teacher = get_user_model().objects.create_user(
            email="teacher@test.com",
            password='1',
            full_name="teacher",
            is_teacher=True
        )
        self.teacher.save()

    def tearDown(self):
        self.user.delete()
        self.teacher.delete()

    def test_auth_user(self):
        user = authenticate(email='test@test.com', password='1')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_image_folder(self):
        filename = 'example.jpg'
        result = 'users/test/test.jpg'
        self.assertEqual(self.user.image_folder(filename), result)

    def test_str_student_with_full_name(self):
        result = 'test_user - test@test.com'
        self.assertEqual(self.user.__str__(), result)

    def test_str_teacher(self):
        result = 'Teacher: teacher - teacher@test.com'
        self.assertEqual(self.teacher.__str__(), result)


class UserSerializerTest(TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        user = User.objects.get(email="test@test.com")
        user.delete()

    def test_UserSerializer(self):
        instance = User.objects.create(
            email="test@test.com",
            password="1",
            full_name="test_user"
        )

        serializer = UserSerializer(instance=instance)
        self.assertEqual(serializer.data['email'], "test@test.com")
        self.assertEqual(serializer.data['full_name'], "test_user")

    def test_UserSerialiser_create(self):
        data = {
            "email": "test@test.com",
            "full_name": 'test_user',
            "password": "1"
        }

        serializer = UserSerializer(data=data)
        self.user = serializer.create(validated_data=data)
        self.assertEqual(self.user.email, data['email'])
        self.assertEqual(self.user.full_name, data['full_name'])

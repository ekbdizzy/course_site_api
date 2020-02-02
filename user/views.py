from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import User
from course.models import Course
from course.serializers import CourseSerializer
from .tasks import user_is_registered_email
from .serializers import UserSerializer, UserAuthSerializer, UserProfileSerializer

from utils.logger import logging


@permission_classes((AllowAny,))
class CreateUserView(APIView):
    authentication_classes = ()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email):
                return Response({"message": "Email is already registered"}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.create(serializer.validated_data)

            # celery send email
            # user_is_registered_email.delay(email)

            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)

        # logging.error(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class AuthenticateUserView(APIView):

    def post(self, request):

        if request.user.is_authenticated:
            return Response({"message": "Please, logout (/api/user/logout)"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserAuthSerializer(data=request.data)
        if serializer.is_valid():
            try:
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                user = User.objects.get(email=email)
                if user.check_password(password):
                    user = authenticate(username=email, password=password)
                    if user:
                        login(request, user)
                        data = serializer.data
                        data['token'] = user.auth_token.key
                        return Response(data, status=status.HTTP_202_ACCEPTED)

                # logging.error(serializer.errors)
                return Response({"message": "Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist:
                # logging.error(serializer.errors)
                return Response({"message": "User is not registered"}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):

    def get(self, request):

        if request.user.is_authenticated:
            user = request.user
            users_courses = Course.objects.filter(students=user)
            course_serializer = CourseSerializer(users_courses, many=True)
            user_serializer = UserProfileSerializer(user)

            course_data = course_serializer.data
            user_data = user_serializer.data
            return Response(data=(course_data, user_data), status=status.HTTP_200_OK)

        else:
            return Response({"message": "User is not authenticated"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        print(request.user)

        if request.user.is_authenticated:
            user = request.user

            serializer = UserProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.update(user, serializer.validated_data)
                data = serializer.data
                return Response(data, status=status.HTTP_200_OK)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "User is not authenticated"}, status=status.HTTP_400_BAD_REQUEST)

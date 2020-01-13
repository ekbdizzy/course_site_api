from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from .models import User
from .tasks import user_is_registered_email
from .serializers import UserSerializer, UserAuthSerializer

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

        logging.error(serializer.errors)
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

                logging.error(serializer.errors)
                return Response({"message": "Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist:
                logging.error(serializer.errors)
                return Response({"message": "User is not registered"}, status=status.HTTP_400_BAD_REQUEST)

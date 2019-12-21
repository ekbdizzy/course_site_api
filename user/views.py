from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login

from .models import User
from .tasks import user_is_registered_email
from .serializers import UserSerializer, UserAuthSerializer


# Create your views here.
class RegisterUserView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():

            email = serializer.validated_data['email']
            if User.objects.filter(email=email):
                return Response({"message": "Email is already registered"}, status=status.HTTP_400_BAD_REQUEST)

            serializer.create(serializer.validated_data)

            # celery send email
            user_is_registered_email.delay(email)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticateUserView(APIView):

    def post(self, request):

        if request.user.is_authenticated:
            return Response({"message": "Please, logout"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserAuthSerializer(data=request.data)
        if serializer.is_valid():
            try:
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login_user = authenticate(username=email, password=password)
                    if login_user:
                        login(request, login_user)
                    return Response(
                        {"message": f"Welcome, {request.user.full_name}"},
                        status=status.HTTP_202_ACCEPTED
                    )

                return Response({"message": "Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"message": "User is not registered"}, status=status.HTTP_400_BAD_REQUEST)

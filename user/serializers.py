from rest_framework import serializers, status
from .models import User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'full_name',
            'email',
        )
        read_only_fields = ('id',)

    email = serializers.EmailField(required=True)


class TeacherSerializer(StudentSerializer):
    is_teacher = serializers.BooleanField(default=True)


class UserSerializer(StudentSerializer):
    class Meta:
        model = User

        fields = (
            'full_name',
            'email',
            'password',
        )

    password = serializers.CharField(required=True)
    write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserAuthSerializer(StudentSerializer):
    class Meta:
        model = User

        fields = (
            'email',
            'password'
        )

from rest_framework import serializers
from rest_framework.authtoken.models import Token

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

    password = serializers.CharField(required=True, write_only=True)
    full_name = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class UserAuthSerializer(UserSerializer):
    class Meta:
        model = User

        fields = (
            'email',
            'password'
        )


class UserProfileSerializer(UserSerializer):
    class Meta:
        model = User

        fields = (
            'full_name',
            'email',
            # 'avatar'
        )

        email = serializers.CharField(required=False)
        full_name = serializers.CharField(required=False)
        # avatar = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        # instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from google_sheets_to_db import settings
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=settings.ACCOUNT_EMAIL_REQUIRED)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    password = serializers.CharField(required=True, style={'input_type': 'password'}, )
    password_repeat = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'}, )

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat',)

    def validate_password(self, password: str) -> str:
        validate_password(password=password, user=User)
        return password

    def validate(self, data: dict) -> dict:
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError(
                "The two password fields didn't match.")
        data.pop('password_repeat')
        return data

    def create(self, validated_data: dict) -> User:
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()

        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        read_only_fields = ('id',)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data: str) -> User:

        user = authenticate(**data)
        if user:
            if user.is_active:
                return user
            raise ValidationError('Account is not activated')
        raise AuthenticationFailed('Invalid credentials.')

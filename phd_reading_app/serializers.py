# Serializers define the API representation.
from django.contrib.auth.models import User, Group
from rest_framework import serializers, request
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field].required = False

    def validate(self, attrs):
        email = attrs['email']
        user = User.objects.filter(email=email).first()

        if not user:
            raise AuthenticationFailed(
                self.error_messages["No active account"],
                'no active account',
            )

        attrs['username'] = user.username
        return super().validate(attrs)

from rest_framework import serializers
from .models import *
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'role', 'created_at', 'is_active']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        if not check_password(password, user.password):
            raise AuthenticationFailed("Invalid password")

        return data


class PredictionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested user information

    class Meta:
        model = Prediction
        fields = ['id', 'image', 'result', 'timestamp', 'location', 'site_name', 'user']

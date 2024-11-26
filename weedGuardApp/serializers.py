from rest_framework import serializers
from .models import *
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    # Set the default value of the role field to 'farmer'
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='farmer')

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'role']

    def create(self, validated_data):
        # Ensure that role is set to 'farmer' if not provided
        role = validated_data.get('role', 'farmer')  # Default to 'farmer' if not provided
        user = User.objects.create(
            fullname=validated_data['fullname'],
            email=validated_data['email'],
            role=role
        )
        user.password = make_password(validated_data['password'])  # Hash the password
        user.save()
        return user

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

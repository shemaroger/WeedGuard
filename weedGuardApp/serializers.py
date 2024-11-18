from rest_framework import serializers
from .models import User, Prediction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'role', 'created_at', 'is_active']


class PredictionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested user information

    class Meta:
        model = Prediction
        fields = ['id', 'image', 'result', 'timestamp', 'location', 'site_name', 'user']

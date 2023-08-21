from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'name', 'surname', 'email', 'username', 'phone_number', 'created', 'last_login', 'fireid']
        # password is for writing purpose only no need to send it back to the user
        extra_kwargs = {'password': {'write_only': True}}

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
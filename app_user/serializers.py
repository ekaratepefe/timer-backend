# app_user/serializers.py

from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email','first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

from rest_framework import serializers
from .models import CustomUser

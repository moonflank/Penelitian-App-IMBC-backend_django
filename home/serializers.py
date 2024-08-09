# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from authapp.models import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'role')  # Sesuaikan field sesuai dengan model Role

class UserProfileSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)  # Gunakan RoleSerializer di sini

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')

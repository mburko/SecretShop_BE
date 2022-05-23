from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import User, UserFollowers

import os


class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'password')

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)


class RegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=128, write_only=True)
	token = serializers.CharField(max_length=255, read_only=True)

	class Meta:
		model = User
		fields = ('id', 'email', 'username', 'password', 'token')
		
	def create(self, validated_data):
		return User.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ("__all__")


class UserFollowerSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserFollowers
		fields = ("__all__")

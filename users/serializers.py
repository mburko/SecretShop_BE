from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import User

import os


class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['login', 'email','password']


class RegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=128, write_only=True)
	token = serializers.CharField(max_length=255, read_only=True)

	class Meta:
		model = User
		fields = ('email', 'login', 'password', 'token')
		
	def create(self, validated_data):
		return User.objects.create_user(**validated_data)


#TODO: Method loginSerializer does not work in the way it is supposed to
class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField(write_only=True)
	password = serializers.CharField(max_length=128, write_only=True)
	token = serializers.CharField(max_length=255, read_only=True)
	
	def validate(self, data):
		email = data.get('email', None)
		password = data.get('password', None)

		if email is None:
			raise serializers.ValidationError(
				detail="Email address is required to log in.")
		if password is None:
			raise serializers.ValidationError(
				detail="Password is required to log in.")

		user = authenticate(email=email, password=password)

		if user is None:
			raise serializers.ValidationError(
				detail="User with this email and password was not found.")

		return {'token': user.token}

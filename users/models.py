from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
	BaseUserManager, PermissionsMixin
from django.db.models.fields import CharField
from django.core.validators import RegexValidator, MinLengthValidator

import jwt

from datetime import datetime
from datetime import timedelta


class UserManager(BaseUserManager):
	def _create_user(self, email, password, is_superuser, role, **extra_fields):
		if not email:
			raise ValueError('No email adress')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.is_superuser = is_superuser
		user.role = role
		user.set_password(password, )
		user.save(using=self._db)
		return user

	def create_user(self, email, password, **extra_fields):
		return self._create_user(email, password, False, 1, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		return self._create_user(email, password, True, 2, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

	FIRST_ROLE = 1
	SECOND_ROLE = 2
	THIRD_ROLE = 3

	ROLES_CHOICES = [
		(FIRST_ROLE, "User"),
		(SECOND_ROLE, "Admin"),
		(THIRD_ROLE, "Premium")
	]

	username = models.CharField(max_length=20,
		blank=False, unique=True, validators=(RegexValidator(
			regex=r'^[a-zA-Z0-9\_\-\.]*$'), MinLengthValidator(5),))
	email = models.EmailField(max_length=40, blank=False, unique=True)
	password = CharField(max_length=256, blank=False)
	avatar = CharField(max_length=256, validators=(RegexValidator(regex=r'^([a-zA-Z0-9\_\-\.]+\\[a-zA-Z0-9\_\-\.]+)+$'),))
	role = models.CharField(max_length=30, blank=True, choices=ROLES_CHOICES, default=FIRST_ROLE)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'password']
	objects = UserManager()

	def __str__(self):
		return self.username

	@property
	def token(self):
		return self._generate_jwt_token()

	def _generate_jwt_token(self):
		import os
		from dotenv import find_dotenv, load_dotenv
		dt = datetime.now() + timedelta(days=5)

		load_dotenv(find_dotenv('./.env'))
		key = os.getenv('JWT_CODE')
		token = jwt.encode({
			'email': self.email,
			'exp': int(dt.timestamp())
		}, key=key, algorithm='HS256')
		return token.decode('utf-8')


class UserFollowers(models.Model):
	user_follower = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		blank=False,
		related_name="user_follower"
	)
	user_following = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		blank=False,
		related_name="user_following"
	)
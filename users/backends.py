from django.core.exceptions import ObjectDoesNotExist
from rest_framework import authentication, exceptions
from users.models import User
import jwt

import os
from dotenv import find_dotenv, load_dotenv


class JWTAuthentication(authentication.BaseAuthentication):
	authentication_header_prefix = 'Bearer'

	def authenticate(self, request):
		request.user = None
		header = authentication.get_authorization_header(
			request=request).split()
		prefix_1 = self.authentication_header_prefix

		if not header or len(header) != 2:
			return None

		prefix_2 = header[0].decode(encoding='utf-8')
		token = header[1].decode(encoding='utf-8')
		if prefix_1.lower() != prefix_2.lower():
			return None

		load_dotenv(find_dotenv(filename='./.env'))
		key = os.getenv(key='JWT_CODE')
		token = jwt.decode(jwt=token, key=key, algorithms=["HS256"])
		
		try:
			user = User.objects.get(email=token['email'])
		except ObjectDoesNotExist:
			raise exceptions.AuthenticationFailed(
				detail="User does not exists")

		return (user, token)

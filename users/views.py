from rest_framework import status
from users.serializers import RegistrationSerializer, UsersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
import jwt
from datetime import datetime
from datetime import timedelta


class RegistrationAPIView(APIView):
	permission_classes = (AllowAny, )
	serializer_class = RegistrationSerializer
	
	def post(self, request):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response({'token': serializer.data.get('token', None)},
				status=status.HTTP_201_CREATED)

		return Response(serializer.errors, 
			status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
	permission_classes = (AllowAny,)

	def post(self, request):
		serializer = request.data

		user = User.objects.filter(email=serializer["email"]).first()

		if user is None:
			raise AuthenticationFailed("User doesn't exist")

		if not user.check_password(serializer["password"]):
			raise AuthenticationFailed("Wrong password")

		import os
		from dotenv import find_dotenv, load_dotenv
		dt = datetime.now() + timedelta(days=30)

		load_dotenv(find_dotenv('./.env'))

		token = jwt.encode({
			'email': user.email,
			'exp': int(dt.timestamp())
		}, key=os.getenv("JWT_CODE"), algorithm='HS256')

		response = Response()
		_cookie_lifetime = 2592000
		response.set_cookie(key="jwt_session", value=token, httponly=True, max_age=_cookie_lifetime)
		response.data = {
			"jwt_session": token
		}

		return response


class UserAPIView(APIView):
	def get(self, request):
		token = request.COOKIES.get("jwt_session")

		if not token:
			return Response({"message:": "Unauthenticated"}, status=status.HTTP_400_BAD_REQUEST)

		import os
		from dotenv import find_dotenv, load_dotenv

		load_dotenv(find_dotenv('./.env'))

		try:
			payload = jwt.decode(token, os.getenv("JWT_CODE"), algorithms=["HS256"])
		except jwt.ExpiredSignatureError:
			return Response({"message:": "Unauthenticated"}, status=status.HTTP_400_BAD_REQUEST)

		user = User.objects.filter(email=payload["email"]).first()

		return Response(RegistrationSerializer(user).data)


class LogOutAPIView(APIView):
	def post(self, request):
		response = Response()
		response.delete_cookie("jwt_session")
		response.data = {
			"message": "Successful log out"
		}
		return response


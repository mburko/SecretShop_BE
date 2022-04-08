from rest_framework import status
from users.serializers import LoginSerializer, \
	RegistrationSerializer
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
	serializer_class = LoginSerializer

	def post(self, request):
		email = request.data["email"]
		password = request.data["password"]

		user = User.objects.filter(email=email).first()

		if user is None:
			raise AuthenticationFailed("User doesn't exist")

		if not user.check_password(password):
			raise AuthenticationFailed("Wrong password")

		import os
		from dotenv import find_dotenv, load_dotenv
		dt = datetime.now() + timedelta(days=30)

		load_dotenv(find_dotenv('./.env'))

		token = jwt.encode({
			'email': user.email,
			'exp': int(dt.timestamp())
		}, key=os.getenv("JWT_CODE"), algorithm='HS256')

		return Response({
			"token": token
		})

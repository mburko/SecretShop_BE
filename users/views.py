from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from users.serializers import RegistrationSerializer, UsersSerializer,\
	ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
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
			return Response(serializer.data,
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
	paginator_class = PageNumberPagination()
	serializer_class = RegistrationSerializer

	def get(self, request):
		queryset = User.objects.all()
		limit = request.GET.get("limit", len(queryset))
		page = request.GET.get("page", None)

		self.paginator_class.page_size = limit
		if page is not None:
			self.paginator_class.page = page

		if not queryset:
			return Response({"message": "Questions not found"}, status=status.HTTP_404_NOT_FOUND)

		serializer = self.serializer_class(self.paginator_class.paginate_queryset(queryset=queryset, request=request),
										   many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class UserAPIGetByIdView(APIView):
	serializer_class = RegistrationSerializer

	def get(self, request, pk):
		try:
			queryset = User.objects.get(pk=pk)
		except ObjectDoesNotExist:
			return Response({"message": "User with such ID doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

		serializer = self.serializer_class(queryset)

		return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileView(APIView):
	serializer_class = ProfileSerializer

	def get(self, request):
		token = request.headers.get("jwt_session")

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

		serializer = self.serializer_class(user)

		return Response(serializer.data, status=status.HTTP_200_OK)


class LogOutAPIView(APIView):
	def post(self, request):
		response = Response()
		response.delete_cookie("jwt_session")
		response.data = {
			"message": "Successful log out"
		}
		return response


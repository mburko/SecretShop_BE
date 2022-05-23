from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from users.serializers import RegistrationSerializer, UsersSerializer,\
	ProfileSerializer, UserFollowerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
from users.models import User, UserFollowers
import jwt
from datetime import datetime
from datetime import timedelta
from secretshop.utils import AuthenticationUtils


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
			return Response({"message": "Users not found"}, status=status.HTTP_404_NOT_FOUND)

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

	@AuthenticationUtils.authenticate
	def get(self, request):
		token = request.headers.get("Authorization")

		import os
		from dotenv import find_dotenv, load_dotenv

		load_dotenv(find_dotenv('./.env'))

		payload = jwt.decode(token, os.getenv("JWT_CODE"), algorithms=["HS256"])

		user = User.objects.filter(email=payload["email"]).first()

		serializer = self.serializer_class(user)

		return Response(serializer.data, status=status.HTTP_200_OK)


class LogOutAPIView(APIView):
	@AuthenticationUtils.authenticate
	def post(self, request):
		response = Response()
		response.delete_cookie("jwt_session")
		response.data = {
			"message": "Successful log out"
		}
		return response


class UserFollowerAPIView(APIView):
	serializer_class = UserFollowerSerializer

	@AuthenticationUtils.authenticate
	def post(self, request):
		request_data = request.data

		if request_data["user_follower"] == request_data["user_following"]:
			return Response({"Error": "Cannot follow yourself"},
							status=status.HTTP_400_BAD_REQUEST)

		try:
			currentFollower = UserFollowers.objects.get(
				user_follower=request_data["user_follower"],
				user_following=request_data["user_following"]
			)
			user_name = User.objects.get(pk=request_data["user_following"])
			UserFollowers.objects.filter(pk=currentFollower.pk).delete()

			return Response({"Message": f"You have successfully unfollowed {user_name}"},
							status=status.HTTP_200_OK)
		except ObjectDoesNotExist:

			serializer = self.serializer_class(data=request_data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data,
								status=status.HTTP_201_CREATED)
			return Response(serializer.errors,
							status=status.HTTP_400_BAD_REQUEST)

	@AuthenticationUtils.authenticate
	def get(self, request):
		queryset = UserFollowers.objects.all()
		if not queryset:
			return Response({"message": "Follows not found"},
							status=status.HTTP_404_NOT_FOUND)

		serializer = self.serializer_class(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class UserFollowerByIdAPIView(APIView):
	serializer_class = UserFollowerSerializer

	@AuthenticationUtils.authenticate
	def get(self, request, pk):
		queryset = UserFollowers.objects.filter(user_follower=pk)

		if not queryset:
			return Response({"message": "You haven't followed yet"},
							status=status.HTTP_404_NOT_FOUND)

		serializer = self.serializer_class(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

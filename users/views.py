from rest_framework import status
from users.serializers import LoginSerializer, \
	RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


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
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			return Response(serializer.data, 
				status=status.HTTP_200_OK)

		return Response(serializer.errors, 
			status=status.HTTP_400_BAD_REQUEST)	

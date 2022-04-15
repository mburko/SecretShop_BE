from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import APIView
from rest_framework import status

from django.db.models import ObjectDoesNotExist
from answers.models import Answers
from answers.serializers import AnswersSerializer


class AnswersEditAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AnswersSerializer
    paginator_class = PageNumberPagination()

    def get(self, request):
        queryset = Answers.objects.all()
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

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

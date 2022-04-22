from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import APIView
from rest_framework import status

from django.db.models import ObjectDoesNotExist
from answers.models import Answers
from answers.serializers import AnswersSerializer, AnswersSerializerForGet


class AnswersEditAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AnswersSerializerForGet
    paginator_class = PageNumberPagination()
    queryset = Answers.objects.all()

    def get(self, request):
        queryset = self.queryset.all()
        if not queryset:
            return Response({"message": "Questions not found"}, status=status.HTTP_404_NOT_FOUND)

        limit = request.GET.get("limit", len(queryset))
        page = request.GET.get("page", None)

        self.paginator_class.page_size = limit
        if page is not None:
            self.paginator_class.page = page

        serializer = AnswersSerializer(self.paginator_class.paginate_queryset(queryset=queryset, request=request),
                                           many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswersEditByIdAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AnswersSerializerForGet
    paginator_class = PageNumberPagination()
    doesnt_exist_message = {"message": "Question doesn't exist"}

    def get(self, request, question_id):
        queryset = Answers.objects.all().filter(question_id=question_id)
        if not queryset:
            return Response(self.doesnt_exist_message, status=status.HTTP_404_NOT_FOUND)

        serializer = AnswersSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            answer = Answers.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(self.doesnt_exist_message, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            answer = Answers.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(self.doesnt_exist_message, status=status.HTTP_404_NOT_FOUND)
        answer.delete()
        return Response({"message": f"Question {pk} was successfully deleted"}, status=status.HTTP_200_OK)


from django.shortcuts import render

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
        question_id = request.GET.get("question_id", None)

        if not question_id:
            return Response({"message": "You haven't enetered question_id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            answer = Answers.objects.filter(question_id=question_id)
        except ObjectDoesNotExist:
            return Response({"message": "This question doesn't have answers yet"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(answer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswersEditByIdAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AnswersSerializer
    doesnt_exist_message = {"message": "Question doesn't exist"}

    def get(self, request, pk):
        try:
            answer = Answers.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(self.doesnt_exist_message, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(answer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            answer = Answers.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(self.doesnt_exist_message, status=status.HTTP_400_BAD_REQUEST)
        answer.delete()
        return Response({"message": f"Questions {pk} was successfully deleted"}, status=status.HTTP_200_OK)

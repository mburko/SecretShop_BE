from django.shortcuts import render
from rest_framework.response import Response
from questions.serializers import QuestionsSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.models import ObjectDoesNotExist
from questions.models import Questions
from questions.serializers import QuestionsSerializer
from rest_framework.decorators import APIView


class QuestionsEditAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = QuestionsSerializer

    def get(self, request):
        questions = Questions.objects.all()

        author_id = request.GET.get('author_id', None)

        if author_id is not None:
            questions = questions.filter(author_id=author_id)
        serializer = self.serializer_class(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionsEditByIdAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = QuestionsSerializer

    def get(self, request, pk):
        try:
            question = Questions.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"message": "Question doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            question = Questions.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"message": "Question doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            question = Questions.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"message": "Question doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        question.delete()
        return Response({"message": f"Questions {pk} was successfully deleted"}, status=status.HTTP_200_OK)


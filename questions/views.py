from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import APIView
from rest_framework import status

from django.db.models import ObjectDoesNotExist
from questions.models import Questions, Tags
from questions.serializers import QuestionsSerializer, TagsSerializer


class QuestionsEditAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = QuestionsSerializer
    paginator_class = PageNumberPagination()

    def get(self, request):
        queryset = Questions.objects.all()
        author_id = request.GET.get('author_id', None)
        limit = request.GET.get("limit", len(queryset))
        page = request.GET.get("page", None)

        self.paginator_class.page_size = limit
        if page is not None:
            self.paginator_class.page = page

        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)

        if not queryset:
            return Response({"message": "Questions not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(self.paginator_class.paginate_queryset(queryset=queryset, request=request), many=True)
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
    paginator_class = PageNumberPagination
    doesnt_exist_message = {"message": "Question doesn't exist"}

    def get(self, request, author_id):
        try:
            queryset = Questions.objects.all().filter(author_id=author_id)
        except ObjectDoesNotExist:
            return Response(self.doesnt_exist_message, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            question = Questions.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(self.doesnt_exist_message, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            question = Questions.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(self.doesnt_exist_message, status=status.HTTP_404_NOT_FOUND)
        question.delete()
        return Response({"message": f"Question {pk} was successfully deleted"}, status=status.HTTP_200_OK)


class TagsEditAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TagsSerializer
    paginator_class = PageNumberPagination()

    def get(self, request):
        limit = request.GET.get("limit", None)
        page = request.GET.get("page", None)
        queryset = Tags.objects.all()

        if limit is not None:
            self.paginator_class.page_size = limit
        if page is not None:
            self.paginator_class.page = page

        if not queryset:
            return Response({"message": "Questions not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(self.paginator_class.paginate_queryset(queryset=queryset, request=request), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagsEditByIdAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TagsSerializer
    doesnt_exist_message = {"message": "Tag doesn't exist"}

    def get(self, request, pk):
        try:
            tag = Tags.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(self.doesnt_exist_message, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            tag = Tags.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(self.doesnt_exist_message, status=status.HTTP_404_NOT_FOUND)
        tag.delete()
        return Response({"message": f"Questions {pk} was successfully deleted"}, status=status.HTTP_200_OK)


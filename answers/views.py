from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import APIView
from rest_framework import status

from django.db.models import ObjectDoesNotExist
from answers.models import Answers, AnswerReaction
from answers.serializers import \
	AnswersSerializer, AnswersSerializerForGet, AnswerReactionSerializer


class AnswersEditAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AnswersSerializerForGet
    paginator_class = PageNumberPagination()
    queryset = Answers.objects.all()

    def get(self, request):
        queryset = self.queryset.all()
        if not queryset:
            return Response(
				data={"message": "Questions not found"}, 
				status=status.HTTP_404_NOT_FOUND)

        limit = request.GET.get("limit", len(queryset))
        page = request.GET.get("page", None)

        self.paginator_class.page_size = limit
        if page is not None:
            self.paginator_class.page = page

        serializer = AnswersSerializer(
			self.paginator_class.paginate_queryset(
				queryset=queryset, 
				request=request),
            many=True)

        return Response(
			data=serializer.data, 
			status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(
			data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
				data=serializer.data, 
				status=status.HTTP_201_CREATED)

        return Response(
			data=serializer.errors, 
			status=status.HTTP_400_BAD_REQUEST)


class AnswersEditByIdAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AnswersSerializerForGet
    paginator_class = PageNumberPagination()
    doesnt_exist_message = {"message": "Question doesn't exist"}

    def get(self, request, question_id):
        queryset = Answers.objects.all().filter(
			question_id=question_id)
        if not queryset:
            return Response(
				data=self.doesnt_exist_message, 
				status=status.HTTP_404_NOT_FOUND)

        serializer = AnswersSerializer(queryset, many=True)
        return Response(serializer.data, 
			status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            answer = Answers.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
				data=self.doesnt_exist_message, 
				status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
			instance=answer, 
			data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
				data=serializer.data, 
				status=status.HTTP_200_OK)

        return Response(
			data=serializer.errors, 
			status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            answer = Answers.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
				data=self.doesnt_exist_message, 
				status=status.HTTP_404_NOT_FOUND)

        answer.delete()
        return Response(
			data={"message": f"Question {pk} was successfully deleted"},
			status=status.HTTP_200_OK)


class AnswerReactionView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AnswerReactionSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            try:
                res = AnswerReaction.objects.get(
                    answer=serializer.data["answer"],
                    user=serializer.data["user"])
                if res.reaction_type == data["reaction_type"]:
                    res.delete()
                else:
                    res.reaction_type = data["reaction_type"]
                    res.save()
            except ObjectDoesNotExist:
                serializer.save()

            number_of_likes = AnswerReaction.objects.filter(
                answer=data["answer"],
                reaction_type=AnswerReaction.ReactionType.LIKE).count()
            number_of_dislikes = AnswerReaction.objects.filter(
                answer=data["answer"],
                reaction_type=AnswerReaction.ReactionType.DISLIKE).count()

            try:
                answer = Answers.objects.get(
                    pk=data["answer"].id)
                answer.number_of_likes = number_of_likes
                answer.number_of_dislikes = number_of_dislikes
                answer.save()

                return Response(
                    data=serializer.data,
                    status=status.HTTP_202_ACCEPTED)

            except ObjectDoesNotExist:
                return Response(
                    data={"Error": "Something is wrong with db."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)

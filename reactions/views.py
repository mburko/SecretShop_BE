from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import APIView
from rest_framework import status

from django.db.models import ObjectDoesNotExist

from reactions.models import QuestionReaction, AnswerReaction
from reactions.serializers import \
    QuestionReactionSerializer, AnswerReactionSerializer


class QuestionReactionSerializer(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionReactionSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data)

        if serializer.is_valid():
            try:
                res = QuestionReaction.objects.get(
                    question=serializer.data["question"],
                    user=serializer.data["user"])
                serializer = self.serializer_class(
                    instance=res, 
                    data=request.data)
            except ObjectDoesNotExist:
                pass
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_202_ACCEPTED)
                
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class AnswerReactionSerializer(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnswerReactionSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data)

        if serializer.is_valid():
            try:
                res = AnswerReaction.objects.get(
                    answer=serializer.data["answer"],
                    user=serializer.data["user"])
                serializer = self.serializer_class(
                    instance=res, 
                    data=request.data)
            except ObjectDoesNotExist:
                pass
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_202_ACCEPTED)
                
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)

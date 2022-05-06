from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import APIView
from rest_framework import status

from django.db.models import ObjectDoesNotExist
from questions.models import Questions, Tags, QuestionReaction
from users.models import User
from questions.serializers import QuestionsSerializer, TagsSerializer,\
    QuestionsAddSerializer, QuestionReactionSerializer

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def request_parsing(string):
    dict_ = {
        '{sh}': '#',
        '{p}': '+',
        '{td}': ':',
        '{qm}': '?',
        '{dog}': '@',
        '{em}': '!',
        '{and}': '&',
        '{rs}': '/',
        '{lb}': '(',
        '{rb}': ')',
        '{lsb}': '[',
        '{rsb}': ']',
    }
    for i in dict_:
        string = string.replace(i, dict_[i])
    return string


class QuestionsEditAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = QuestionsAddSerializer
    paginator_class = PageNumberPagination()
    order_by_list = ("fame_index", "date_of_publication", "number_of_likes", "number_of_comments", "number_of_views")

    def get(self, request):
        queryset = Questions.objects.all()
        limit = request.GET.get("limit", 42)  # len(queryset))
        page = request.GET.get("page", None)
        # ordering_field = request.GET.get("order_by", "fame_index")
        # order_direction = "" if request.GET.get("direction", "desc") == "asc" else "-"
        try: #Formulating the tag list, and add the '#' symbol to the beginning
            search_tags = ["#" + i for i in request_parsing(request.GET.get("tags")).split(',')]
        except AttributeError:
            search_tags = None
        search = request.GET.get("search_query")
        search_vector = SearchVector("title", weight="A") + SearchVector("text_body", weight="B")
        search_query = SearchQuery(search)
        author = request.GET.get("author")
        self.paginator_class.page_size = limit
        if page is not None:
            self.paginator_class.page = page

        if search_tags is not None:  # Search for questions that contain at least one of the listed tags
            tags_id = Tags.objects.filter(tag_name__in=search_tags).values_list("id")
            queryset = queryset.filter(tags__in=tags_id).order_by("-number_of_likes")

        if author is not None:  # Search for questions written by the selected author
            try:
                author_id = User.objects.filter(username__exact=author).values_list("id")[0]
            except IndexError:
                pass
            else:
                queryset = queryset.filter(author_id__exact=author_id).order_by("-number_of_likes")

        # if ordering_field in self.order_by_list:
        if search is not None:  # Search for questions by words
            queryset = queryset.annotate(rank=SearchRank(search_vector, search_query)) \
                .filter(rank__gte=0.3) \
                .order_by("-rank")

        if not queryset:
            return Response({"message": "Questions not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionsSerializer(
            self.paginator_class.paginate_queryset(queryset=queryset.distinct(), request=request), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED)

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class QuestionsEditByIdAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = QuestionsSerializer
    paginator_class = PageNumberPagination
    order_by_list = (
        "fame_index",
        "date_of_publication",
        "number_of_likes",
        "number_of_comments",
        "number_of_views"
    )
    doesnt_exist_message = {"message": "Question doesn't exist"}

    def get(self, request, author_id):
        queryset = Questions.objects.filter(author_id=author_id)

        if not queryset:
            return Response(
                data=self.doesnt_exist_message,
                status=status.HTTP_404_NOT_FOUND)

        ordering_field = request.GET.get("order_by", "fame_index")
        order_direction = "" if request.GET.get("direction", "desc") == "asc" \
            else "-"
        if ordering_field in self.order_by_list:
            queryset = queryset.order_by(f"{order_direction}{ordering_field}")

        serializer = self.serializer_class(queryset, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            question = Questions.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                data=self.doesnt_exist_message,
                status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            instance=question,
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
            question = Questions.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                data=self.doesnt_exist_message,
                status=status.HTTP_404_NOT_FOUND)

        question.delete()
        return Response(
            data={"message": f"Question {pk} was successfully deleted"},
            status=status.HTTP_200_OK)


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
            return Response(
                data={"message": "Questions not found"},
                status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
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


class TagsEditByIdAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TagsSerializer
    doesnt_exist_message = {"message": "Tag doesn't exist"}

    def get(self, request, pk):
        try:
            tag = Tags.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                data=self.doesnt_exist_message,
                status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(tag)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            tag = Tags.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                data=self.doesnt_exist_message,
                status=status.HTTP_404_NOT_FOUND)
        tag.delete()
        return Response(
            data={"message": f"Questions {pk} was successfully deleted"},
            status=status.HTTP_200_OK)


class QuestionReactionView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = QuestionReactionSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            try:
                res = QuestionReaction.objects.get(
                    question=data["question"],
                    user=data["user"])
                if res.reaction_type == data["reaction_type"]:
                    res.delete()
                else:
                    res.reaction_type = data["reaction_type"]
                    res.save()
            except ObjectDoesNotExist:
                serializer.save()

            number_of_likes = QuestionReaction.objects.filter(
                question=data["question"],
                reaction_type=QuestionReaction.ReactionType.LIKE).count()
            number_of_dislikes = QuestionReaction.objects.filter(
                question=data["question"],
                reaction_type=QuestionReaction.ReactionType.DISLIKE).count()

            try:
                question = Questions.objects.get(
                    pk=data["question"].id)
                question.number_of_likes = number_of_likes
                question.number_of_dislikes = number_of_dislikes
                question.save()

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

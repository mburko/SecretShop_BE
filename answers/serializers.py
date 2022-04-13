from rest_framework import serializers
from answers.models import Answers


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = (
            "id",
            "author_id",
            "question_id",
            "text_body",
            "date_of_publication",
            "number_of_likes",
            "number_of_dislikes"
        )

from rest_framework import serializers
from questions.models import Questions


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = (
            "id",
            "author_id",
            "title",
            "text_body",
            "date_of_publication"
        )
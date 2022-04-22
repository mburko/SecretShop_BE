from rest_framework import serializers
from questions.models import Questions, Tags


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = (
            "id",
            "author_id",
            "title",
            "text_body",
            "date_of_publication",
            "tags"
        )

class QuestionsAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = (
            "id",
            "author_id",
            "title",
            "text_body",
            "tags"
        )

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = (
            "id",
            "tag_name"
        )

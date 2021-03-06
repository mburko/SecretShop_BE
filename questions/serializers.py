from rest_framework import serializers
from questions.models import Questions, Tags, QuestionReaction


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = (
            "id",
            "author_id",
            "title",
            "text_body",
            "date_of_publication",
            "tags",
            "number_of_views",
            "number_of_comments",
            "number_of_likes",
            "number_of_dislikes"
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


class QuestionReactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionReaction
		fields = (
			'reaction_type',
			'user',
			'question'
		)

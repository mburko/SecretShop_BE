from rest_framework import serializers
from answers.models import Answers, AnswerReaction


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = (
            "id",
            "author_id",
            "question_id",
            "text_body",
            "date_of_publication"
        )


class AnswersSerializerForGet(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = (
            "id",
            "author_id",
            "question_id",
            "text_body"
        )


class AnswerReactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = AnswerReaction
		fields = (
			'reaction_type',
			'user',
			'answer'
		)

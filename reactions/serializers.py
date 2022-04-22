from dataclasses import fields
from rest_framework import serializers

from reactions.models import QuestionReaction, AnswerReaction


class QuestionReactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionReaction
		fields = (
			'reaction_type',
			'user',
			'question'
		)


class AnswerReactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = AnswerReaction
		fields = (
			'reaction_type',
			'user',
			'answer'
		)
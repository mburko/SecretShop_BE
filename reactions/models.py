from django.db import models

from users.models import User
from questions.models import Questions
from answers.models import Answers


class ReactionType(models.IntegerChoices):
	DISLIKE = 0
	LIKE = 1


class QuestionReaction(models.Model):
	reaction_type = models.IntegerField(choices=ReactionType)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Questions, on_delete=models.CASCADE)


class AnswerReaction(models.Model):
	reaction_type = models.IntegerField(choices=ReactionType)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answers, on_delete=models.CASCADE)
	
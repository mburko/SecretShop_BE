from datetime import datetime

from django.db import models
from django.core.validators import MinLengthValidator

from users.models import User
from questions.models import Questions


class Answers(models.Model):
    author_id = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  blank=False,
                                  related_name="answer_author")
    question_id = models.ForeignKey(Questions,
                                    on_delete=models.CASCADE,
                                    blank=False)
    text_body = models.CharField(
        max_length=1500,
        blank=False,
        validators=(MinLengthValidator(20),))
    date_of_publication = models.DateTimeField(
        blank=True,
        default=datetime.now)
    number_of_likes = models.IntegerField(
        blank=True,
        default=0)
    number_of_dislikes = models.IntegerField(
        blank=True,
        default=0)
    fame_index = models.FloatField(
        blank=True,
        default=1)
    users_reactions = models.ManyToManyField(User,
                                             through="AnswerReaction",
                                             related_name="reacted_on_answer")


class AnswerReaction(models.Model):
    class ReactionType(models.IntegerChoices):
        DISLIKE = 0
        LIKE = 1

    reaction_type = models.IntegerField(
        choices=ReactionType.choices)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    answer = models.ForeignKey(Answers,
                               on_delete=models.CASCADE)

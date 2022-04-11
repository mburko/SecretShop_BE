from datetime import datetime

from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from users.models import User


class Questions(models.Model):
    OPENED = 1
    CLOSED = 0

    STATUS_CHOICES = [
        (OPENED, 'Opened'),
        (CLOSED, 'Closed'),
    ]

    author_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    title = models.CharField(max_length=255, blank=False, validators=(MinLengthValidator(20), ))
    text_body = models.CharField(max_length=1500, blank=False, validators=(MinLengthValidator(20),))
    status = models.CharField(max_length=2, blank=True, choices=STATUS_CHOICES, default=OPENED)
    date_of_publication = models.DateTimeField(blank=True, default=datetime.now())
    number_of_views = models.IntegerField(blank=True, default=0)
    number_of_comments = models.IntegerField(blank=True, default=0)
    number_of_likes = models.IntegerField(blank=True, default=0)
    number_of_dislikes = models.IntegerField(blank=True, default=0)
    fame_index = models.FloatField(blank=True, default=1)

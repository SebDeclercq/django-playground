from datetime import timedelta
from django.db import models
from django.db.models import CharField, DateTimeField, IntegerField, ForeignKey
from django.utils import timezone


class Question(models.Model):
    question_text: CharField = models.CharField(max_length=200)
    pub_date: DateTimeField = models.DateTimeField('date_published')

    @property
    def is_new(self) -> bool:
        return self.pub_date >= timezone.now() - timedelta(hours=1)

    def __str__(self) -> str:
        return self.question_text


class Choice(models.Model):
    question: ForeignKey = models.ForeignKey(
        Question, on_delete=models.CASCADE
    )
    choice_text: CharField = models.CharField(max_length=200)
    votes: IntegerField = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text

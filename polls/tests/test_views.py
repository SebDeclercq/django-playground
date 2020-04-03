from typing import List, Set
import time
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from django.utils import timezone
import pytest
from polls.models import Question


@pytest.mark.django_db
class TestIndex:
    def test_get_no_question(self, client: Client) -> None:
        r: HttpResponse = client.get(reverse('polls:index'))
        assert r.status_code == 200
        assert 'No polls yet' in r.content.decode('utf-8')
        assert len(r.context['object_list']) == 0

    def test_get_with_questions(self, client: Client) -> None:
        questions: List[Question] = []
        for i in range(10):
            questions.append(
                Question(
                    question_text=f'question_{i}', pub_date=timezone.now()
                )
            )
            questions[-1].save()
            time.sleep(0.01)
        r: HttpResponse = client.get(reverse('polls:index'))
        questions_on_page: Set[Question] = set(r.context['object_list'])
        assert questions_on_page == set(questions[-5:])


@pytest.mark.django_db
class TestDetail:
    def test_get_one_question(self, client: Client) -> None:
        q: Question = Question(question_text='Hello', pub_date=timezone.now())
        q.save()
        r: HttpResponse = client.get(reverse('polls:detail', args=(q.id,)))
        assert q.question_text in r.content.decode('utf-8')

    def test_get_404(self, client: Client) -> None:
        r: HttpResponse = client.get(reverse('polls:detail', args=(1,)))
        assert r.status_code == 404

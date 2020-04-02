from django.db.models import Manager
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question


def index(request: HttpRequest) -> HttpResponse:
    latest_questions: Manager[Question] = Question.objects.order_by(
        '-pub_date'
    )[:5]
    return render(
        request, 'index.html', {'latest_questions': latest_questions},
    )


def details(request: HttpRequest, question_id: int) -> HttpResponse:
    question: Question = get_object_or_404(Question, pk=question_id)
    return render(request, 'details.html', {'question': question})


def results(request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(
        f'You are looking at the results of question {question_id}'
    )


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(f'You are voting on question {question_id}')

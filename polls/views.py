from django.db.models import Manager
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
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
    question: Question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    question: Question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice: Choice = question.choice_set.get(
            pk=request.POST['choice']
        )
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            'details.html',
            {'question': question, 'error_message': 'Please select a choice'},
        )
    else:
        selected_choice += 1
        selected_choice.save()
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,))
        )

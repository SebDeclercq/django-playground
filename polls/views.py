from __future__ import annotations
from typing import List
from django.db.models import Manager
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name: str = 'index.html'
    context_object_name: str = 'latest_questions'

    def get_queryset(self) -> Manager[Question]:
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model: type = Question
    template_name: str = 'details.html'


class ResultsView(generic.DetailView):
    model: type = Question
    template_name: str = 'results.html'


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

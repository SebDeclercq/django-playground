from typing import List
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model: type = Choice
    extra: int = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines: List[type] = [ChoiceInline]
    list_display: List[str] = ['question_text', 'pub_date', 'is_new']
    list_filter: List[str] = ['pub_date']
    search_fields: List[str] = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

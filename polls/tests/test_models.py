import datetime as dt
from unittest.mock import Mock
from _pytest.monkeypatch import MonkeyPatch
from django.utils import timezone
import django
from polls.models import Choice, Question


class TestQuestion:
    def test_is_new(self) -> None:
        question: Question = Question(pub_date=timezone.now())
        assert question.is_new is True

    def test_is_not_new(self) -> None:
        question: Question = Question(
            pub_date=dt.datetime(1999, 1, 1, tzinfo=dt.timezone.utc)
        )
        assert question.is_new is False

    def test_str(self) -> None:
        hw: str = 'Hello World'
        question: Question = Question(question_text=hw)
        assert str(question) == hw

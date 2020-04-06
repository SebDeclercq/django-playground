from typing import Any
from django.core.management.base import (
    BaseCommand,
    CommandError,
    CommandParser,
)
from ._private import Csv2Db


class Command(BaseCommand):
    help: str = (
        'Parse a CSV file extracted from BIBLIO_SUPPORT'
        'and insert the Standards in database'
    )

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--csv', type=str, dest='path_to_csv', help='The CSV path'
        )

    def handle(self, *args: Any, **options: Any) -> None:
        try:
            csv_to_db = Csv2Db()
            csv_to_db.parse(options['path_to_csv'])
        except KeyError:
            raise CommandError('Please provide the CSV path')

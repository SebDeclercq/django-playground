from datetime import datetime
from pathlib import Path
from typing import Dict, List
import csv
from django.core.exceptions import ValidationError
from csv_to_genie2.models import File, Standard


class Csv2Db:
    def parse(self, csv_path: str) -> None:
        with Path(csv_path).open() as fh:
            reader: csv.DictReader = csv.DictReader(fh, delimiter='\t')
            for record in reader:
                self.save_record(record)

    def insert(self, records: List[Dict[str, str]]) -> List[Standard]:
        assert isinstance(records, list)
        return [self.save_record(record) for record in records]

    def save_record(self, record: Dict[str, str]) -> Standard:
        std, _ = Standard.objects.get_or_create(
            numdos=record['numdos'],
            refdoc=record['refdoc'],
            datoff=datetime.strptime(record['datoff'], '%Y%m%d').date(),
            ancart=record['ancart'],
        )
        File(
            numdos=record['numdos'],
            numdosvl=record['numdosvl'],
            format=record['format'],
            verling=record['verling'],
            standard_id=std.id,
        ).save()
        return std

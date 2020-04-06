from datetime import datetime
from pathlib import Path
from typing import Dict
import csv
from django.core.exceptions import ValidationError
from csv_to_genie2.models import File, Standard


class Csv2Db:
    def parse(self, csv_path: str) -> None:
        with Path(csv_path).open() as fh:
            reader: csv.DictReader = csv.DictReader(fh, delimiter='\t')
            for record in reader:
                self.save_record(record)

    def save_record(self, record: Dict[str, str]) -> None:
        try:
            std: Standard = Standard(
                numdos=record['numdos'],
                refdoc=record['refdoc'],
                datoff=datetime.strptime(record['datoff'], '%Y%m%d').date(),
                ancart=record['ancart'],
            )
            std.save()
            File(
                numdos=record['numdos'],
                numdosvl=record['numdosvl'],
                format=record['format'],
                verling=record['verling'],
                standard_id=std.id,
            ).save()
        except ValidationError as e:
            if 'this Numdos already exists' in str(e):
                pass
            else:
                raise e()

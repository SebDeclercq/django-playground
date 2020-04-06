from pathlib import Path
from django.core.management import call_command, CommandError
from py._path.local import LocalPath
import pytest
from csv_to_genie2.models import File, Standard


CSV_CONTENT: str = '''numdos	refdoc	datoff	ancart	numdosvl	format	verling
XS126450	ISO 14001:2015	20150915	ISO14001	XS126450	PDFC	F
XS126450	ISO 14001:2015	20150915	ISO14001	XE126450	PDFC	E
XS022560	ISO 9001:2015	20150915	ISO9001	XS022560	PDFC	F
XS022560	ISO 9001:2015	20150915	ISO9001	XE022560	PDFC	E
XS022560	ISO 9001:2015	20150915	ISO9001	XE022560	XML	E
XS022560	ISO 9001:2015	20150915	ISO9001	XS022560	XML	F
XS126450	ISO 14001:2015	20150915	ISO14001	XS126450	XML	F
XS126450	ISO 14001:2015	20150915	ISO14001	XE126450	XML	E'''


class TestCsv2DbCommand:
    @pytest.mark.django_db
    def test_func_complete(self, tmp_path: LocalPath) -> None:
        csv_file: LocalPath = tmp_path / 'fake.csv'
        csv_file.write_text(CSV_CONTENT)
        call_command('csv_to_db', csv=str(csv_file))
        for idx, line in enumerate(CSV_CONTENT.split('\n')):
            if idx == 0:
                continue
            numdos, *_ = line.split('\t')
            std: Standard = Standard.objects.get(numdos=numdos)
            assert std.numdos == numdos
            assert len(std.file_set.all()) >= 1
            for file_ in std.file_set.all():
                assert isinstance(file_, File)
                assert file_.format in (File.PDFC, File.PDFI, File.XML)
                assert file_.verling in (
                    File.ENGLISH,
                    File.FRENCH,
                    File.BILINGUAL,
                )

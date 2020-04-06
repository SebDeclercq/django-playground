from django.core.exceptions import ValidationError
import pytest
from csv_to_genie2.models import File, Standard


@pytest.mark.django_db
class TestStandard:
    def test_valid_numdos(self) -> None:
        std: Standard = Standard(
            numdos='XS123456', refdoc='ISO 123:2020', ancart='ISO123'
        )
        std.save()
        assert std.id == 1

    def test_invalid_numdos(self) -> None:
        with pytest.raises(ValidationError, match=r'NUMDOS'):
            Standard(numdos='HELLO WORLD').save()


class TestFile:
    def test_invalid_numdosvl(self) -> None:
        with pytest.raises(ValidationError, match=r'NUMDOS'):
            File(numdosvl='HELLO WORLD').full_clean()

    def test_invalid_format(self) -> None:
        with pytest.raises(ValidationError, match=r'PPTX.*choice'):
            File(
                numdos='XS123456',
                numdosvl='XS123456',
                verling=File.FRENCH,
                format='PPTX',
            ).full_clean()

    def test_invalid_verling(self) -> None:
        with pytest.raises(ValidationError, match=r'XXX.*choice'):
            File(
                numdos='XS123456',
                numdosvl='XS123456',
                verling='XXX',
                format=File.XML,
            ).full_clean()

    @pytest.mark.django_db
    def test_valid(self) -> None:
        numdos: str = 'XS123456'
        std: Standard = Standard(
            numdos=numdos, refdoc='ISO 123:2020', ancart='ISO123'
        )
        std.save()
        f: File = File(
            numdos=numdos,
            numdosvl=numdos,
            verling=File.BILINGUAL,
            format='PDFC',
            standard_id=std.id,
        )
        f.save()
        assert f.id == 1
        assert f.standard.numdos == numdos

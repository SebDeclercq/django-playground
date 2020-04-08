from datetime import date
from typing import Any, Dict, List
from django.http import HttpResponse
from rest_framework.test import APIClient
import pytest
from csv_to_genie2.models import File, Standard


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def std() -> Standard:
    return Standard.objects.create(
        numdos='XS123456',
        refdoc='HELLO WORLD',
        ancart='HW1',
        datoff=date(2020, 1, 1),
    )


@pytest.fixture
def files(std: Standard) -> List[File]:
    files: List[File] = []
    for i, verling in enumerate(('E', 'F', 'F/E')):
        for fmt in ('PDFC', 'XML'):
            file_: File = File.objects.create(
                numdos=std.numdos,
                numdosvl=std.numdos,
                format=fmt,
                verling=verling,
                standard=std,
            )
            files.append(file_)
    return files


class TestApi:
    @pytest.mark.django_db
    def test_get_standards(
        self, client: APIClient, std: Standard, files: List[File]
    ) -> None:
        res: HttpResponse = client.get('/genie2/api/standards/')
        assert res.status_code == 200
        assert len(res.json()) == 1
        data: Dict[str, Any] = res.json()[0]
        assert data['ancart'] == std.ancart
        assert len(data['file_set']) == len(std.file_set.all())
        url_to_file: str = data['file_set'][0]
        res = client.get(url_to_file)
        assert res.status_code == 200
        assert res.json().get('format') == files[0].format

    @pytest.mark.django_db
    def test_filter_file_one_filter(
        self, client: APIClient, files: List[File]
    ) -> None:
        verling: str = 'F/E'
        res: HttpResponse = client.get(
            '/genie2/api/files/', {'verling': verling}
        )
        assert res.status_code == 200
        assert len(res.json()) == 2
        for i, data in enumerate(res.json()):
            assert data.get('numdosvl') == files[i].numdosvl
            assert data.get('format') == files[i].format
            assert data.get('verling') == verling

    @pytest.mark.django_db
    def test_filter_file_many_filters(
        self, client: APIClient, files: List[File]
    ) -> None:
        verling: str = 'F/E'
        numdosvl: str = 'XS000000'
        res: HttpResponse = client.get(
            '/genie2/api/files/', {'verling': verling, 'numdosvl': numdosvl},
        )
        assert res.status_code == 200
        assert len(res.json()) == 0, '2 F/E verlings but not numdosvl XS00000'

    @pytest.mark.django_db
    def test_standard_filter(self, client: APIClient, std: Standard) -> None:
        url: str = '/genie2/api/standards/'
        res: HttpResponse = client.get(url, {'ancart': 'XS000000'})
        assert res.status_code == 200
        assert len(res.json()) == 0
        res = client.get(url, {'ancart': std.ancart})
        assert res.status_code == 200
        assert len(res.json()) == 1

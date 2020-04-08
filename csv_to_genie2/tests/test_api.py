from datetime import date
from typing import Any, Dict
from django.http import HttpResponse
from rest_framework.test import APIClient
import pytest
from csv_to_genie2.models import File, Standard


@pytest.fixture
def client() -> APIClient:
    return APIClient()


class TestApi:
    @pytest.mark.django_db
    def test_get_standards(self, client: APIClient) -> None:
        std: Standard = Standard.objects.create(
            numdos='XS123456',
            refdoc='HELLO WORLD',
            ancart='HW1',
            datoff=date(2020, 1, 1),
        )
        fil: File = File.objects.create(
            numdos=std.numdos,
            numdosvl=std.numdos,
            format='PDFC',
            verling='E',
            standard=std,
        )
        res: HttpResponse = client.get('/genie2/api/standards/')
        assert res.status_code == 200
        assert len(res.json()) == 1
        data: Dict[str, Any] = res.json()[0]
        assert data['ancart'] == std.ancart
        assert len(data['file_set']) == len(std.file_set.all())
        url: str = data['file_set'][0].replace('http://testserver', '')
        res = client.get(url)
        assert res.status_code == 200
        assert res.json().get('format') == fil.format

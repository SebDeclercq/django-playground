from __future__ import annotations
from typing import Any, Callable, Dict, List
from django.db.models import Manager
from django.http import HttpRequest
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response
from csv_to_genie2.csv_parser import Csv2Db
from csv_to_genie2.models import File, Standard
from csv_to_genie2.serializers import FileSerializer, StandardSerializer


class StandardViewSet(viewsets.ModelViewSet):
    queryset: Manager[Standard] = Standard.objects.all().order_by('numdos')
    serializer_class: type = StandardSerializer
    lookup_field: str = 'numdos'
    filter_backends: List[str] = [DjangoFilterBackend]
    filterset_fields: List[str] = ['numdos', 'refdoc', 'datoff', 'ancart']
    permission_classes: List[str] = [permissions.IsAuthenticated]


class FileViewSet(viewsets.ModelViewSet):
    queryset: Manager[File] = File.objects.all().order_by('numdos', 'numdosvl')
    serializer_class: type = FileSerializer
    filter_backends: List[type] = [DjangoFilterBackend]
    filterset_fields: List[str] = ['numdos', 'numdosvl', 'verling', 'format']
    permission_classes: List[str] = [permissions.IsAuthenticated]


class ActionView(views.APIView):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        '''Constructor'''
        self.ACTIONS: Dict[str, Callable] = {'insert': self._insert}
        super().__init__(*args, **kwargs)

    def post(self, request: HttpRequest, action: str) -> Response:
        try:
            return self.ACTIONS[action](request)
        except KeyError:
            return Response(
                {'msg': f'Unknown action "{action}"'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def _insert(self, request: HttpRequest) -> Response:
        csv_to_db: Csv2Db = Csv2Db()
        stds: List[Standard] = csv_to_db.insert(request.data)
        result = []
        for std in stds:
            serialized: StandardSerializer = StandardSerializer(
                std, context={'request': request}
            )
            result.append(serialized.data)
        return Response(result)

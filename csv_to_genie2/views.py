from __future__ import annotations
from typing import Dict, List
from django.db.models import Manager
from django.shortcuts import render
from rest_framework import permissions, viewsets
from csv_to_genie2.models import File, Standard
from csv_to_genie2.serializers import FileSerializer, StandardSerializer


class StandardViewSet(viewsets.ModelViewSet):
    queryset: Manager[Standard] = Standard.objects.all().order_by('numdos')
    serializer_class: type = StandardSerializer
    lookup_field: str = 'numdos'


class FileViewSet(viewsets.ModelViewSet):
    queryset: Manager[File] = File.objects.all().order_by('numdos', 'numdosvl')
    serializer_class: type = FileSerializer

    def get_queryset(self) -> Manager[File]:
        if self.request.query_params:
            for key, value in self.request.query_params.items():
                filters: Dict[str, List[str]] = {f'{key}__in': [value]}
            return File.objects.filter(**filters)
        else:
            return super().get_queryset()

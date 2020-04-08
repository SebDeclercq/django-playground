from __future__ import annotations
from typing import Dict, List
from django.db.models import Manager
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
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

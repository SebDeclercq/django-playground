from __future__ import annotations
from typing import List
from django.db.models import Manager
from django.shortcuts import render
from rest_framework import permissions, viewsets
from csv_to_genie2.models import File, Standard
from csv_to_genie2.serializers import FileSerializer, StandardSerializer


class StandardViewSet(viewsets.ModelViewSet):
    queryset: Manager[Standard] = Standard.objects.all().order_by('numdos')
    serializer_class: type = StandardSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset: Manager[File] = File.objects.all().order_by('numdos', 'numdosvl')
    serializer_class: type = FileSerializer

from __future__ import annotations
from typing import Any, Sequence
from django.db.models import Manager
from graphene_django.types import DjangoObjectType
from graphql.execution.base import ResolveInfo
import graphene
from csv_to_genie2.models import File, Standard


class FileType(DjangoObjectType):
    '''Object representing a "SUPPORT" record from Genie 2.'''

    class Meta:
        model: type = File


class StandardType(DjangoObjectType):
    '''Object representing a "BIBLIO" record from Genie 2.'''

    files: graphene.List = graphene.List(FileType)

    class Meta:
        model: type = Standard
        exclude_fields: Sequence[str] = ('file_set',)

    def resolve_files(self, info: ResolveInfo, **kwargs: Any) -> Manager[File]:
        return self.file_set.all()

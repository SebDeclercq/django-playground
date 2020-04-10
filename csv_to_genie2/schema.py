from __future__ import annotations
from typing import Any
from django.db.models import Manager
from graphene_django.types import DjangoObjectType
import graphene
from graphql.execution.base import ResolveInfo
from csv_to_genie2.models import File, Standard


class FileType(DjangoObjectType):
    class Meta:
        model: type = File


class StandardType(DjangoObjectType):
    class Meta:
        model: type = Standard


class Query(graphene.ObjectType):
    all_files: graphene.List = graphene.List(FileType)
    all_standards: graphene.List = graphene.List(StandardType)

    def resolve_all_files(
        self, info: ResolveInfo, **kwargs: Any
    ) -> Manager[File]:
        return File.objects.all()

    def resolve_all_standards(
        self, info: ResolveInfo, **kwargs: Any
    ) -> Manager[Standard]:
        return Standard.objects.all()


schema: graphene.Schema = graphene.Schema(query=Query)

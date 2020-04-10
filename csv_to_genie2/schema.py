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
    file: graphene.Field = graphene.Field(
        FileType, id=graphene.Int(), numdosvl=graphene.String(),
    )
    standard: graphene.Field = graphene.Field(
        StandardType, id=graphene.Int(), numdos=graphene.String(),
    )

    def resolve_all_files(
        self, info: ResolveInfo, **kwargs: Any
    ) -> Manager[File]:
        return File.objects.all()

    def resolve_all_standards(
        self, info: ResolveInfo, **kwargs: Any
    ) -> Manager[Standard]:
        return Standard.objects.all()

    def resolve_file(self, info: ResolveInfo, **kwargs: Any) -> File:
        if id_ := kwargs.get('id'):
            return File.objects.get(pk=id_)
        if numdosvl := kwargs.get('numdosvl'):
            return File.objects.get(numdosvl=numdosvl)

    def resolve_standard(self, info: ResolveInfo, **kwargs: Any) -> Standard:
        if id_ := kwargs.get('id'):
            return Standard.objects.get(pk=id_)
        if numdos := kwargs.get('numdos'):
            return Standard.objects.get(numdos=numdos)


schema: graphene.Schema = graphene.Schema(query=Query)

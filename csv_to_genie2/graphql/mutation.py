from __future__ import annotations
from datetime import date
from typing import Optional
from graphene_django import DjangoObjectType
import graphene
from csv_to_genie2.graphql.types import FileType, StandardType
from csv_to_genie2.models import File, Standard


class CreateStandard(graphene.Mutation):
    class Arguments:
        numdos = graphene.String(required=True)
        refdoc = graphene.String()
        ancart = graphene.String()
        datoff = graphene.Date()

    standard: graphene.Field = graphene.Field(StandardType)

    def mutate(
        self,
        info,
        numdos: str,
        refdoc: str = '?',
        ancart: str = '?',
        datoff: date = date.today(),
    ) -> CreateStandard:
        std, _ = Standard.objects.get_or_create(
            numdos=numdos, refdoc=refdoc, ancart=ancart, datoff=datoff
        )
        return CreateStandard(standard=std)


class UpdateStandard(CreateStandard):
    def mutate(
        self,
        info,
        numdos: str,
        refdoc: str = '',
        ancart: str = '',
        datoff: Optional[date] = None,
    ) -> UpdateStandard:
        std: Standard = Standard.objects.get(numdos=numdos)
        if refdoc:
            std.refdoc = refdoc
        if ancart:
            std.ancart = ancart
        if datoff is not None:
            std.datoff = datoff
        std.save()
        return UpdateStandard(standard=std)


class DeleteStandard(graphene.Mutation):
    class Arguments:
        numdos = graphene.String(required=True)

    ok: graphene.Field = graphene.Boolean()

    def mutate(self, info, numdos: str) -> DeleteStandard:
        try:
            std: StandardType = Standard.objects.get(numdos=numdos)
            std.delete()
        except Standard.DoesNotExist:
            pass
        return DeleteStandard(ok=True)


class Mutation(graphene.ObjectType):
    create_standard: graphene.Field = CreateStandard.Field()
    update_standard: graphene.Field = UpdateStandard.Field()
    delete_standard: graphene.Field = DeleteStandard.Field()

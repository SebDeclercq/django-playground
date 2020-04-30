from __future__ import annotations
from datetime import date
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
        print(std)
        return CreateStandard(standard=std)


class Mutation(graphene.ObjectType):
    create_standard: graphene.Field = CreateStandard.Field()

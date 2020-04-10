import graphene
from csv_to_genie2 import schema


class Query(schema.Query, graphene.ObjectType):
    pass


schema: graphene.Schema = graphene.Schema(query=Query)

from graphene_django.types import DjangoObjectType
from csv_to_genie2.models import File, Standard


class FileType(DjangoObjectType):
    '''Object representing a "SUPPORT" record from Genie 2.'''

    class Meta:
        model: type = File


class StandardType(DjangoObjectType):
    '''Object representing a "BIBLIO" record from Genie 2.'''

    class Meta:
        model: type = Standard

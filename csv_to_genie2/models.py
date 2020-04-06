from typing import Any, List, Tuple
import re
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CharField, DateField, ForeignKey


def numdos_validator(numdos: str) -> None:
    if not re.match(r'^[A-Z]{2}\d{6}$', numdos):
        raise ValidationError('Not a NUMDOS')


class Standard(models.Model):
    numdos: CharField = models.CharField(
        max_length=8, validators=[numdos_validator], unique=True
    )
    refdoc: CharField = models.CharField(max_length=200)
    datoff: DateField = models.DateField(null=True, blank=True)
    ancart: CharField = models.CharField(max_length=200)

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)


class File(models.Model):
    PDFC: str = 'PDFC'
    PDFI: str = 'PDFI'
    XML: str = 'XML'
    ENGLISH: str = 'E'
    FRENCH: str = 'F'
    BILINGUAL: str = 'F/E'
    FORMATS: List[Tuple[str, str]] = [
        (PDFC, 'PDFC'),
        (PDFI, 'PDFI'),
        (XML, 'XML'),
    ]
    VERLINGS: List[Tuple[str, str]] = [
        (ENGLISH, 'E'),
        (FRENCH, 'F'),
        (BILINGUAL, 'F/E'),
    ]

    numdos: CharField = models.CharField(
        max_length=8, validators=[numdos_validator]
    )
    numdosvl: CharField = models.CharField(
        max_length=8, validators=[numdos_validator]
    )
    format: CharField = models.CharField(
        max_length=4, choices=FORMATS, default=PDFC
    )
    verling: CharField = models.CharField(
        max_length=3, choices=VERLINGS, default=ENGLISH
    )
    standard: ForeignKey = models.ForeignKey(
        Standard, on_delete=models.CASCADE
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)
